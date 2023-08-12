import logging
import traceback

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.departments import DepartmentCreateUpdateSerializer, DepartmentRetrieveSerializer, \
    DepartmentTreeListSerializer, DepartmentBaseRetrieveSerializer
from system.models import Department
from utils.drf_utils.model_utils import generate_object_tree_data, page_with_drf_original_format

logger = logging.getLogger('evotrack')


class DepartmentNameFilter(filters.FilterSet):
    """
    自定义过滤器类，实现对部门名称进行模糊搜索(不区分大小写)
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', label='部门名称(模糊搜索且不区分大小写)')

    class Meta:
        model = Department
        fields = ['name']


@extend_schema(tags=['部门管理'])
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all().order_by('-id')
    filterset_class = DepartmentNameFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'create']:
            return DepartmentCreateUpdateSerializer
        elif self.action in ['retrieve', 'destroy']:
            return DepartmentRetrieveSerializer
        elif self.action == 'list':
            return DepartmentBaseRetrieveSerializer
        elif self.action == 'get_department_tree_list':
            return DepartmentTreeListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username, updated_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)

    @extend_schema(responses=unite_response_format_schema('create-department',
                                                          DepartmentCreateUpdateSerializer()))
    def create(self, request, *args, **kwargs):
        """
        create department
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    def list(self, request, *args, **kwargs):
        """
        select department list
        """
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_200_OK)

    @extend_schema(responses=unite_response_format_schema('select-department-detail',
                                                          DepartmentRetrieveSerializer()))
    def retrieve(self, request, *args, **kwargs):
        """
        select department detail
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True, status=status.HTTP_200_OK)

    @extend_schema(
        responses=unite_response_format_schema('update-department-detail',
                                               DepartmentCreateUpdateSerializer()))
    def update(self, request, *args, **kwargs):
        """
        update department detail
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', success=True)

    @extend_schema(
        responses=unite_response_format_schema('partial-update-department-detail',
                                               DepartmentCreateUpdateSerializer()))
    def partial_update(self, request, *args, **kwargs):
        """
        partial update department detail
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        delete department
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(responses=unite_response_format_schema('get-department-tree-list',
                                                          DepartmentTreeListSerializer()))
    @action(methods=['get'], detail=False, url_path='tree')
    def get_department_tree_list(self, request, *args, **kwargs):
        """
        select department tree list
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

