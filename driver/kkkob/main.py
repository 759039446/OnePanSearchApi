import asyncio
import json
from urllib.parse import urljoin

import aiohttp

from driver import error


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
    async def search(keyword: str, token: str, endpoint: str, path: str):
        payload = {
            "name": keyword,
            "token": token,
        }
        res = await KKKOB._request(
            endpoint, "POST", path,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload
        )
        return res.get('list')

    @staticmethod
    async def search_batch( keyword: str,token: str, endpoint: str, search_paths: list):
        results = await asyncio.gather(*(KKKOB.search(keyword, token, endpoint, x) for x in search_paths))
        merged_results = [item for sublist in results for item in sublist]
        return merged_results


if __name__ == '__main__':
    endpoint = "http://p.kkkob.com/"


    async def asyncio_run():
        token = await KKKOB.getToken(endpoint)
        list = await KKKOB.search("庆余年", token, endpoint,"/v/api/search")
        #list = await KKKOB.search_batch("庆余年", token, endpoint,  [
        #    "/v/api/search",
        #    "/v/api/getDJ",
        #    "/v/api/getJuzi",
        #    "/v/api/getXiaoyu",
        #    "/v/api/getSearchX"
        #])
        print(json.dumps(list, ensure_ascii=False))


    asyncio.run(asyncio_run())
