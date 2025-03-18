from urllib.parse import urljoin

from driver.model.search_result import SearchResult
from utils.http_template_util import send_aio_request_template


class FunPan:
    @staticmethod
    async def search(keyword: str, endpoint: str, path: str, **keywords) -> list[SearchResult]:
        url = urljoin(endpoint, path)
        template = {
            "name": "",
            "response_json_path": "data",
            "method": "POST",
            "url": url,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{\n  \"style\": \"get\",\n  \"datasrc\": \"search\",\n  \"query\": {\n    \"id\": \"\",\n    \"datetime\": \"\",\n    \"courseid\": 1,\n    \"categoryid\": \"\",\n    \"filetypeid\": \"\",\n    \"filetype\": \"\",\n    \"reportid\": \"\",\n    \"validid\": \"\",\n    \"searchtext\": \"{{keyword}}\"\n  },\n  \"page\": {\n    \"pageSize\": 100,\n    \"pageIndex\": 1\n  },\n  \"order\": {\n    \"prop\": \"sort\",\n    \"order\": \"desc\"\n  },\n  \"message\": \"请求资源列表数据\"\n}"
        }
        try:
            res = await send_aio_request_template(template, keyword=keyword, **keywords)
        except Exception as e:
            print(f"发送模板请求失败||  请求模板：\n{template}\n错误信息：{e}")
            return []
        results = []
        for item in res[0]:
            # 确保所有字段存在（使用dict.get处理缺失字段）
            results.append(SearchResult(
                id=item.get('id', ''),
                name=item.get('title', '').replace('<em>','').replace('</em>', ''),
                url=item.get('url', ''),
                type=item.get('course', ''),
                pwd=item.get('extcode', ''),
                fromSite=keywords.get('from_site', '')
            ))
        return results
