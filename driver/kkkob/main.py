import asyncio
import json
import re
import traceback
from dataclasses import asdict
from urllib.parse import urljoin
from driver.model.search_result import SearchResult
import aiohttp

from driver import error
from utils.pan_type_util import get_pan_type


def parse_links(data: str):
    lines = data.split('\n')
    pattern = re.compile(r'链接：(https?://\S+)(?:\s+提取码：(\S+))?')
    results = []
    for line in lines:
        match = pattern.search(line.strip())
        if match:
            link = match.group(1)
            pwd = match.group(2) or ''
        else:
            link = line.strip()
            pwd = ''
        results.append({
            "url": link,
            "pwd": pwd,
            'type': get_pan_type(link)
        })
    return results


class KKKOB:
    def __init__(self, ):
        self.endpoint = 'http://p.kkkob.com/'
        self.token = ''

        self.search_paths = [
            "/v/api/search",
            "/v/api/getDJ",
            "/v/api/getJuzi",
            "/v/api/getXiaoyu",
            "/v/api/getSearchX"
        ]

    @staticmethod
    def _isBadRequest(self, r, msg, key="code", value=200, message_key="message"):
        # 是否为不好的请求
        if r[key] != value:
            raise error.ServerError(msg + ":" + r[message_key])

    @staticmethod
    async def _request(endpoint: str, method: str, path: str, *args, **kwargs) -> dict:
        url = urljoin(endpoint, path)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, *args, **kwargs) as response:
                return await response.json()

    @staticmethod
    async def getToken(endpoint: str):
        res = await KKKOB._request(
            endpoint, "GET", "/v/api/getToken",
            headers={"Content-Type": "application/json"},
        )
        return res.get("token")

    @staticmethod
    async def search(keyword: str, token: str, endpoint: str, path: str, **keywords) -> list[SearchResult]:
        payload = {
            "name": keyword,
            "token": token,
        }
        try:
            res = await KKKOB._request(
                endpoint, "POST", path,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=payload
            )
        except Exception as e:
            # traceback.print_exc()
            return []
            # 转换原始数据到实体模型
        raw_list = res.get('list', [])
        results = []
        for item in raw_list:
            parsed = parse_links(item.get('answer'))
            for parsed_item in parsed:
                # 确保所有字段存在（使用dict.get处理缺失字段）
                results.append(SearchResult(
                    id=item.get('id', ''),
                    name=item.get('question', ''),
                    url=parsed_item.get('url', ''),
                    type=parsed_item.get('type', ''),
                    pwd=parsed_item.get('pwd', ''),
                    fromSite=keywords.get('from_site', '')
                ))
        return results


