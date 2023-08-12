# -*- coding: utf-8 -*-
# @File    : custom_json_response.py
# @Software: PyCharm
# @Description:
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer


class JsonResponse(Response):
    """
    自定义接口响应数据格式类
    1.在视图类中的APIView中使用该JsonResponse返回响应数据
    2.ModelViewSet、Mixin下派生的APIView类、views.APIView都需要自己重写并返回JsonResponse格式的数据
    """

    def __init__(self, success=None, msg=None, data=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(None, status=status)

        if isinstance(data, serializers.Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        self.data = {'success': success, 'message': msg, 'data': data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


def unite_response_format_schema(name: str, serializer_class_obj=None, is_null_data=False):
    """
    统一响应体数据格式
    @param name: diy name
    @param serializer_class_obj: 序列化器类对象
    @param is_null_data: data字段是否为null
    @return:
    """
    if is_null_data:
        # 无数据返回
        serializer_class = None
        return {
            200: {
                'type': 'object',
                'properties': {
                    'success': {
                        'type': 'boolean',
                        'description': '操作是否成功',
                        'example': True,
                    },
                    'message': {
                        'type': 'string',
                        'description': '业务提示消息',
                        'example': 'success',
                    },
                    'data': {
                        'type': 'null',
                        'description': '数据',
                        'example': serializer_class,
                    }
                }
            }
        }
    return inline_serializer(name, fields={'success': serializers.BooleanField(help_text='操作是否成功', default=True),
                                           'message': serializers.CharField(help_text='业务提示消息',
                                                                            default='success'),
                                           'data': serializer_class_obj
                                           })
