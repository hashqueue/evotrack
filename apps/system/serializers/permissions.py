from rest_framework import serializers

from system.models import Permission
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from utils.drf_utils.model_utils import get_obj_child_ids


class PermissionCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def update(self, instance, validated_data):
        parent = validated_data.get('parent', False)
        if parent and parent.id == instance.id:
            raise serializers.ValidationError('父权限不能为其本身.')
        ids = set()
        get_obj_child_ids(instance.id, Permission, ids)
        # print(ids)
        if parent and parent.id in ids:
            raise serializers.ValidationError('父权限不能为其子权限.')
        return super().update(instance, validated_data)

    def validate(self, attrs):
        component = attrs.get('component')
        path = attrs.get('path')
        parent = attrs.get('parent', False)
        perm_type = attrs.get('perm_type')
        if parent:
            if perm_type in [1, 2]:
                if perm_type == 1:
                    if not (path and component):
                        raise serializers.ValidationError(
                            '新增或修改菜单权限时, 组件路径、路由path为必填项.')
                elif perm_type == 2:
                    if not path:
                        raise serializers.ValidationError(
                            '新增或修改目录权限时, 路由path为必填项.')
                if Permission.objects.get(id=parent.id).perm_type == 3:
                    raise serializers.ValidationError('(菜单|目录)的父权限必须为(菜单|目录)权限.')
                if path and path.startswith('/'):
                    raise serializers.ValidationError('非根权限的path不能以/开头.')
            if perm_type == 3:
                if Permission.objects.get(id=parent.id).perm_type == 3:
                    raise serializers.ValidationError('按钮的父权限必须为(菜单|目录)权限.')
        else:
            if perm_type in [1, 2]:
                # 没有传parent, 说明修改的是根权限
                if perm_type == 1:
                    if not (path and component):
                        raise serializers.ValidationError(
                            '新增或修改菜单权限时, 组件路径、路由path为必填项.')
                elif perm_type == 2:
                    if component:
                        raise serializers.ValidationError('根权限为目录时组件路径必须为空.')
                    if not path:
                        raise serializers.ValidationError(
                            '新增或修改目录权限时, 路由path为必填项.')
                if path and (not path.startswith('/')):
                    raise serializers.ValidationError('根权限的path必须以/开头.')
            elif perm_type == 3:
                raise serializers.ValidationError('根权限不能为按钮权限.')
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class PermissionBaseRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionBaseTreeSerializer(PermissionBaseRetrieveSerializer):
    children = PermissionBaseRetrieveSerializer(many=True, read_only=True)


class PermissionTreeSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    next = serializers.CharField(read_only=True)
    previous = serializers.CharField(read_only=True)
    results = PermissionBaseTreeSerializer(read_only=True)
    total_pages = serializers.IntegerField(read_only=True)
    page = serializers.IntegerField(read_only=True)
    page_size = serializers.IntegerField(read_only=True)

    class Meta:
        model = Permission
        fields = ('count', 'next', 'previous', 'results', 'total_pages', 'page', 'page_size')


class GetPermissionsWithRoleIdsSerializer(serializers.ModelSerializer):
    menu_permissions = PermissionBaseRetrieveSerializer(many=True, read_only=True)
    button_permissions = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Permission
        fields = ('menu_permissions', 'button_permissions')
        read_only_fields = ('menu_permissions', 'button_permissions')


class PermissionRetrieveSerializer(PermissionBaseRetrieveSerializer):
    parent = PermissionBaseRetrieveSerializer()

    class Meta:
        model = Permission
        fields = '__all__'


class GetAllPermissionSerializer(serializers.ModelSerializer):
    results = PermissionBaseRetrieveSerializer(many=True, read_only=True)
    count = serializers.IntegerField(help_text='权限总数量')

    class Meta:
        model = Permission
        fields = ('results', 'count')
