def get_obj_child_ids(parent: int, models_class_name, ids: set):
    """
    获取models模型的子id集合
    :param parent: models模型类ID
    :param models_class_name: models模型对象类
    :param ids: 默认为空集合
    """
    objs = models_class_name.objects.filter(parent=parent)
    for obj in objs:
        ids.add(obj.id)
        get_obj_child_ids(obj.id, models_class_name, ids)


def convert_tree2list(tree_data):
    """
    将树形结构数据转换为列表结构数据, 列表结构数据中的每一项不能包含children
    @param tree_data:
    @return:
    """
    order_list_data = []
    for item in tree_data:
        if item.get('children'):
            children = item.pop('children')
            order_list_data.append(item)
            order_list_data.extend(convert_tree2list(children))
        else:
            order_list_data.append(item)
    return order_list_data


def generate_object_tree_data(p_serializer_data, is_convert_tree2list=False):
    """
    生成对象树数据
    @param p_serializer_data:
    @param is_convert_tree2list: 是否将树形结构数据转换为 可以根据列表索引就能看到父子关系的列表结构数据
    @return:
    """
    tree_dict = {}
    tree_data = []
    for item in p_serializer_data:
        tree_dict[item['id']] = item
    for item_id in tree_dict:
        if tree_dict.get(item_id).get('parent'):
            pid = tree_dict.get(item_id).get('parent')
            # 父权限的完整数据
            parent_data = tree_dict.get(pid)
            if parent_data:
                # 如果有children就直接追加数据，没有则添加children并设置默认值为[]，然后追加数据
                parent_data.setdefault('children', []).append(tree_dict.get(item_id))
        else:
            # item没有parent, 放在最顶层
            tree_data.append(tree_dict.get(item_id))
    if is_convert_tree2list:
        order_list_data = convert_tree2list(tree_data)
        return order_list_data
    data = {
        'count': len(tree_data),
        'next': None,
        'previous': None,
        'results': tree_data,
        'total_pages': 1,
        'page': 1,
        'page_size': 10,
    }
    return data


def page_with_drf_original_format(self, p_request):
    """
    按照drf原始分页格式返回数据
    @param self:
    @param p_request:
    @return:
    """
    page = self.paginate_queryset(p_request)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        res = self.get_paginated_response(serializer.data)
        return res.data
    serializer = self.get_serializer(p_request, many=True)
    return serializer.data
