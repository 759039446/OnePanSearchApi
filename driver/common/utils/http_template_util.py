import re

from driver.common.utils.http_util import send_request, aio_request

from jsonpath_ng import parse
import json


def custom_format(template, ignore, **kwargs):
    pattern = re.compile(r'\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}')
    return pattern.sub(
        lambda m: (
            str(kwargs[m.group(1)])  # 存在时直接替换
            if m.group(1) in kwargs
            else (m.group(0) if not ignore else "")  # 不存在时根据 ignore 决定保留或清空
        ),
        template
    )


def format_dict(dict_data, format_params: dict):
    if isinstance(dict_data, dict):
        # 如果值是字典，递归格式化
        formatted_value = {}
        for sub_key, sub_value in dict_data.items():
            formatted_value[format_dict(sub_key, format_params)] = format_dict(sub_value, format_params)
    elif isinstance(dict_data, str):
        formatted_value = custom_format(dict_data,False, **format_params)
    else:
        formatted_value = dict_data
    return formatted_value


def is_valid_json(json_string):
    """
    校验并转换json字符串
    """
    try:
        json_object = json.loads(json_string)
    except ValueError:
        return json_string, False
    return json_object, True


def send_request_template(template_config: dict, **kwargs):
    if kwargs:
        conf = format_dict(template_config, kwargs)
    else:
        conf = template_config
    try:
        result = send_request(conf.get('method'),
                              conf.get('url'),
                              headers=conf.get('headers'),
                              data=conf.get('body'))
    except Exception as e:
        print(f"发送模板请求失败||  请求模板：\n{conf}\n错误信息：{e}")
        return None
    result, is_json = is_valid_json(result)
    if not is_json:
        return result
    response_json_path = template_config.get('response_json_path')
    if response_json_path and len(response_json_path) > 0:
        jsonpath_expr = parse(response_json_path)
        # 提取数据
        matches = jsonpath_expr.find(result)
        result = [match.value for match in matches]
    return result


async def send_aio_request_template(template_config: dict, **kwargs):
    if kwargs:
        conf = format_dict(template_config, kwargs)
    else:
        conf = template_config
    try:
        result = await aio_request(conf.get('method'),
                                   conf.get('url'),
                                   headers=conf.get('headers'),
                                   data=conf.get('body'), ssl=False)
    except Exception as e:
        print(f"发送模板请求失败||  请求模板：\n{conf}\n错误信息：{e}")
        return None
    result, is_json = is_valid_json(result)
    if not is_json:
        return result
    response_json_path = template_config.get('response_json_path')
    if response_json_path and len(response_json_path) > 0:
        jsonpath_expr = parse(response_json_path)
        # 提取数据
        matches = jsonpath_expr.find(result)
        result = [match.value for match in matches]
    return result


if __name__ == '__main__':
    template = {
        "name": "",
        "response_json_path": "data",
        "method": "POST",
        "url": "https://v.funletu.com/search",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{\n  \"style\": \"get\",\n  \"datasrc\": \"search\",\n  \"query\": {\n    \"id\": \"\",\n    \"datetime\": \"\",\n    \"courseid\": 1,\n    \"categoryid\": \"\",\n    \"filetypeid\": \"\",\n    \"filetype\": \"\",\n    \"reportid\": \"\",\n    \"validid\": \"\",\n    \"searchtext\": \"{{keyword}}\"\n  },\n  \"page\": {\n    \"pageSize\": 10,\n    \"pageIndex\": 1\n  },\n  \"order\": {\n    \"prop\": \"sort\",\n    \"order\": \"desc\"\n  },\n  \"message\": \"请求资源列表数据\"\n}"
    }
    print(send_request_template(template, keyword='重生'))
