# -*- coding: utf-8 -*-
# @File    : custom_permissions.py
# @Software: PyCharm
# @Description:
# import re
from rest_framework import permissions


class RbacPermission(permissions.BasePermission):
    """
    自定义权限类
    """

    def has_permission(self, request, view):
        """演示环境禁止删除数据"""
        if request.method == 'DELETE':
            return False
        return True
        # 如果用户是超级用户, 则放开权限
        # 只用作系统初始化时通过python3 manage.py createsuperuser注册的superuser用户添加初始数据时使用
        # if request.user.is_superuser:
        #     return True

    # def has_object_permission(self, request, view, obj):
    #     """
    #     对象级别的权限控制
    #     @param request:
    #     @param view:
    #     @param obj:
    #     @return:
    #     """
    #     pass
