from collections import defaultdict


def format_dict(dict_data, format_params: dict):
    """
    通过变量的方式（{xxx}  xx为变量）为dict 数据格式化
    :param dict_data:
    :param format_params:
    :return:
    """
    if isinstance(dict_data, dict):
        # 如果值是字典，递归格式化
        formatted_value = {}
        for sub_key, sub_value in dict_data.items():
            formatted_value[format_dict(sub_key, format_params)] = format_dict(sub_value, format_params)
    elif isinstance(dict_data, str):
        formatted_value = dict_data.format_map(defaultdict(str) | format_params)
    else:
        formatted_value = dict_data
    return formatted_value
