# -*- coding: utf-8 -*-
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from system.views.user import MyTokenObtainPairView, UserRegisterView, UserViewSet
from system.views.department import DepartmentViewSet
from system.views.permission import PermissionViewSet
from system.views.role import RoleViewSet

router = routers.DefaultRouter()
# 如果视图类中没有指定queryset，则需要手动指定basename
router.register(prefix=r'departments', viewset=DepartmentViewSet, basename='department')
router.register(prefix=r'permissions', viewset=PermissionViewSet, basename='permission')
router.register(prefix=r'roles', viewset=RoleViewSet, basename='role')
router.register(prefix=r'users', viewset=UserViewSet, basename='user')
urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('', include(router.urls)),
]
