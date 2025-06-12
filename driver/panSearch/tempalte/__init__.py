from urllib.parse import urljoin

from driver.panSearch.model.search_result import SearchResult
from driver.common.utils.http_template_util import send_aio_request_template
from driver.common.utils.pan_type_util import get_pan_type

FUN_PAN = "funPan"
GET_API = "GET_API"
GET_API_2 = "GET_API_2"
GET_API_3 = "GET_API_3"
GET_API_4 = "GET_API_4"

templates={
    FUN_PAN:{
            "name": "",
            "response_json_path": "data",
            "method": "POST",
            "url": "{{url}}",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{\n  \"style\": \"get\",\n  \"datasrc\": \"search\",\n  \"query\": {\n    \"id\": \"\",\n    \"datetime\": \"\",\n    \"courseid\": 1,\n    \"categoryid\": \"\",\n    \"filetypeid\": \"\",\n    \"filetype\": \"\",\n    \"reportid\": \"\",\n    \"validid\": \"\",\n    \"searchtext\": \"{{keyword}}\"\n  },\n  \"page\": {\n    \"pageSize\": 100,\n    \"pageIndex\": 1\n  },\n  \"order\": {\n    \"prop\": \"sort\",\n    \"order\": \"desc\"\n  },\n  \"message\": \"请求资源列表数据\"\n}"
        },
    GET_API:{
        "name": "",
        "response_json_path": "data",
        "method": "GET",
        "url": "{{url}}{{keyword}}",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": ""
    },
    GET_API_2: {
        "name": "",
        "response_json_path": "",
        "method": "GET",
        "url": "{{url}}{{keyword}}",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": ""
    },
    GET_API_3:{
        "name": "",
        "response_json_path": "data[0]",
        "method": "GET",
        "url": "{{url}}{{keyword}}",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": ""
    },
}


class Template:
    @staticmethod
    async def search(keyword: str, endpoint: str, path: str, temp_name: str, id_field:str,title_field:str,url_field:str, pwd_field:str, **keywords) -> list[SearchResult]:
        url = urljoin(endpoint, path)
        template = templates.get(temp_name, {})
        if template is None:
            print(f"模板不存在：{temp_name}")
            return []
        try:
            res = await send_aio_request_template(template, keyword=keyword,url=url, **keywords)
        except Exception as e:
            print(f"发送模板请求失败||  请求模板：\n{template}\n错误信息：{e}")
            return []
        results = []
        if res is None or len(res) == 0:
            return results
        try:
            if len(template.get("response_json_path")) != 0:
                res = res[0]
            for item in res:
                if isinstance(item, list) and len(item) > 0:
                    item = item[0]
                # 确保所有字段存在（使用dict.get处理缺失字段）
                results.append(SearchResult(
                    id=item.get(id_field, ''),
                    name=item.get(title_field, '').replace('<em>','').replace('</em>', ''),
                    url=item.get(url_field, ''),
                    type=get_pan_type(item.get(url_field, '')),
                    pwd=item.get(pwd_field, ''),
                    fromSite=keywords.get('from_site', ''),
                    code="0"
                ))
        except Exception as e:
            print(f"解析模板结果失败||  请求模板：{keywords.get('from_site', '')}\n{template}\n错误信息：{e}")
            return []
        return results
