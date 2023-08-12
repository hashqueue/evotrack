from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.django_utils.base_model import BaseModel


class Permission(BaseModel):
    """
    权限
    """
    PERM_TYPE_CHOICES = ((1, '菜单'), (2, '目录'), (3, '按钮'))
    name = models.CharField(max_length=64, unique=True, verbose_name="权限名称", help_text='权限名称')
    perm_type = models.PositiveSmallIntegerField(choices=PERM_TYPE_CHOICES, verbose_name='权限类型',
                                                 help_text='权限类型')
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父权限",
                               help_text='父权限')
    icon = models.CharField(max_length=64, blank=True, default='', verbose_name="图标", help_text='图标')
    component = models.CharField(max_length=255, blank=True, default='', verbose_name='组件路径',
                                 help_text='组件路径')
    path = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name='路由path',
                            help_text='路由path')
    redirect = models.CharField(max_length=255, blank=True, default='', verbose_name='路由重定向path',
                                help_text='路由重定向path')
    is_visible = models.BooleanField(blank=True, null=True, verbose_name='是否显示', help_text='是否显示')

    class Meta:
        db_table = 'sys_perm'
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(BaseModel):
    """
    角色：用于权限绑定
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色名", help_text='角色名')
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="权限", help_text='权限')
    desc = models.CharField(max_length=64, blank=True, default='', verbose_name="描述", help_text='描述')

    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Department(BaseModel):
    """
    部门
    """
    name = models.CharField(max_length=128, verbose_name="部门名称", help_text='部门名称')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父部门",
                               help_text='父部门')

    class Meta:
        db_table = 'sys_dept'
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class User(AbstractUser):
    GENDER_CHOICES = ((1, "男"), (2, "女"))
    nick_name = models.CharField(max_length=20, blank=True, default='', verbose_name="昵称", help_text='昵称')
    gender = models.PositiveSmallIntegerField(blank=True, null=True, choices=GENDER_CHOICES, verbose_name="性别",
                                              help_text='性别')
    avatar = models.ImageField(upload_to="avatars/", default=f"avatars/ninja.png", max_length=128, blank=True,
                               verbose_name="头像", help_text='头像')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门",
                                   help_text='部门')
    position = models.CharField(max_length=64, blank=True, default='', verbose_name="职位", help_text='职位')
    roles = models.ManyToManyField(Role, blank=True, verbose_name="角色", help_text='角色')

    class Meta:
        db_table = 'sys_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
