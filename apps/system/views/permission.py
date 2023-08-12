import logging
import traceback

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.permissions import PermissionCreateUpdateSerializer, PermissionRetrieveSerializer, \
    GetPermissionsWithRoleIdsSerializer, PermissionTreeSerializer, PermissionBaseRetrieveSerializer, \
    PermissionBaseTreeSerializer, GetAllPermissionSerializer
from system.models import Permission, Role
from utils.drf_utils.model_utils import generate_object_tree_data, page_with_drf_original_format

logger = logging.getLogger('evotrack')


class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', label='权限名称(模糊搜索且不区分大小写)')

    class Meta:
        model = Permission
        fields = ['name', 'perm_type']


@extend_schema(tags=['权限管理'])
class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('-id')
    filterset_class = PermissionFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'create']:
            return PermissionCreateUpdateSerializer
        elif self.action in ['retrieve', 'destroy']:
            return PermissionRetrieveSerializer
        elif self.action == 'list':
            return PermissionBaseRetrieveSerializer
        elif self.action == 'get_current_user_permissions':
            return PermissionBaseRetrieveSerializer
        elif self.action == 'get_permission_tree_list':
            return PermissionBaseTreeSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username, updated_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)

    @extend_schema(responses=unite_response_format_schema('create-permission',
                                                          PermissionCreateUpdateSerializer()))
    def create(self, request, *args, **kwargs):
        """
        create permission
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    def list(self, request, *args, **kwargs):
        """
        select permission list
        """
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_200_OK)

    @extend_schema(responses=unite_response_format_schema('select-permission-detail',
                                                          PermissionRetrieveSerializer()))
    def retrieve(self, request, *args, **kwargs):
        """
        select permission detail
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_200_OK)

    @extend_schema(
        responses=unite_response_format_schema('update-permission-detail',
                                               PermissionCreateUpdateSerializer()))
    def update(self, request, *args, **kwargs):
        """
        update permission detail
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True)

    @extend_schema(
        responses=unite_response_format_schema('partial-update-permission-detail',
                                               PermissionCreateUpdateSerializer()))
    def partial_update(self, request, *args, **kwargs):
        """
        partial update permission detail
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        delete permission
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        responses=unite_response_format_schema('get-user-permissions',
                                               GetPermissionsWithRoleIdsSerializer()))
    @action(methods=['get'], detail=False, url_path='get-user-permissions')
    def get_current_user_permissions(self, request, pk=None, version=None):
        """
        获取当前登录用户的权限
        """
        permissions = Permission.objects.filter(
            id__in=Role.objects.filter(id__in=self.request.user.roles.values_list('id')).values_list(
                'permissions')).all()
        # print(permissions.query)
        # 获取权限list
        permissions_serializer = self.get_serializer(permissions, many=True)
        button_permissions = []
        menu_permissions = []
        for item in permissions_serializer.data:
            if item.get('perm_type') in [1, 2]:
                menu_permissions.append(item)
            else:
                button_permissions.append(item.get('name'))
        try:
            menu_permissions = generate_object_tree_data(menu_permissions, is_convert_tree2list=True)
        except Exception as e:
            logger.info(f'生成当前用户拥有的权限数据时报错: {e}\n{traceback.format_exc()}')
            menu_permissions = []
        return JsonResponse(data={'menu_permissions': menu_permissions,
                                  'button_permissions': button_permissions}, msg='success', success=True)

    @extend_schema(responses=unite_response_format_schema('get-permission-tree-list',
                                                          PermissionTreeSerializer()))
    @action(methods=['get'], detail=False, url_path='tree')
    def get_permission_tree_list(self, request, *args, **kwargs):
        """
        select permission tree list
        """
        queryset = self.filter_queryset(self.get_queryset())
        try:
            serializer = self.get_serializer(queryset, many=True)
            results = generate_object_tree_data(serializer.data)
            return JsonResponse(data=results, msg='success', success=True)
        except Exception as e:
            # 生成tree型数据报错时，按照非tree格式、drf原始分页格式来返回数据
            logger.info(f'生成树类型的部门数据时报错: {e}\n{traceback.format_exc()}')
            data = page_with_drf_original_format(self, queryset)
            return JsonResponse(data=data, msg='success', success=True)

    @extend_schema(responses=unite_response_format_schema('get-all-permissions', GetAllPermissionSerializer()))
    @action(methods=['get'], detail=False, url_path='all')
    def get_all_permissions(self, request, pk=None, version=None):
        """
        查询所有权限列表
        """
        serializer = PermissionBaseRetrieveSerializer(self.queryset, many=True, context={'request': request})
        return JsonResponse(data={'results': serializer.data, 'count': len(serializer.data)}, msg='success',
                            success=True)
