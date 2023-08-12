from rest_framework import serializers

from system.models import Department
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from utils.drf_utils.model_utils import get_obj_child_ids


class DepartmentCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def update(self, instance, validated_data):
        parent = validated_data.get('parent', False)
        if parent:
            if parent.id == instance.id:
                raise serializers.ValidationError('父部门不能为其本身.')
            ids = set()
            get_obj_child_ids(instance.id, Department, ids)
            # print(ids)
            if parent.id in ids:
                raise serializers.ValidationError('父部门不能为其子部门.')
        return super().update(instance, validated_data)


class DepartmentBaseRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentBaseTreeListSerializer(DepartmentBaseRetrieveSerializer):
    children = DepartmentBaseRetrieveSerializer(many=True, read_only=True)


class DepartmentTreeListSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    next = serializers.CharField(read_only=True)
    previous = serializers.CharField(read_only=True)
    results = DepartmentBaseTreeListSerializer(read_only=True)
    total_pages = serializers.IntegerField(read_only=True)
    page = serializers.IntegerField(read_only=True)
    page_size = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ('count', 'next', 'previous', 'results', 'total_pages', 'page', 'page_size')


class DepartmentRetrieveSerializer(DepartmentBaseRetrieveSerializer):
    parent = DepartmentBaseRetrieveSerializer()

    class Meta:
        model = Department
        fields = '__all__'
