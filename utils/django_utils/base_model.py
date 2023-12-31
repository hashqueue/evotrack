# -*- coding: utf-8 -*-
# @File    : base_model.py
# @Software: PyCharm
# @Description:
from django.db import models


class BaseModel(models.Model):
    """
    数据库表公共字段
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    created_by = models.CharField(max_length=150, verbose_name='创建人', help_text='创建人')
    updated_by = models.CharField(max_length=150, verbose_name='最后修改人', help_text='最后修改人')

    class Meta:
        # 设置当前模型类为抽象类，用于其他模型类来继承，数据库迁移时不会创建当前模型类的表
        abstract = True
        verbose_name = '公共字段表'
