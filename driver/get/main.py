import asyncio
import json
from urllib.parse import urljoin

import aiohttp

from driver import error


class KKKOB:
    def __init__(self):
        self.endpoint = 'http://p.kkkob.com/'
        self.token = ''
        self.headers = {
            "Content-Type": "application/json",
        }
        self.formHeader = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        self.search_paths = [
            "/v/api/search",
            "/v/api/getDJ",
            "/v/api/getJuzi",
            "/v/api/getXiaoyu",
            "/v/api/getSearchX"
        ]

    def _isBadRequest(self, r, msg, key="code", value=200, message_key="message"):
        # 是否为不好的请求
        if r[key] != value:
            raise error.ServerError(msg + ":" + r[message_key])

    async def _request(self, method: str, path: str, *args, **kwargs) -> dict:
        url = urljoin(self.endpoint, path)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, *args, **kwargs) as response:
                return await response.json()

    async def getToken(self):
        res = await self._request(
            "GET", "/v/api/getToken", headers=self.headers,
        )
        self.token = res.get("token")

    async def search(self, keyword: str, path="/v/api/search"):
        payload = {
            "name": keyword,
            "token": self.token,
        }
        res = await self._request(
            "POST", path, headers=self.formHeader, data=payload
        )
        return res.get('list')

    async def search_batch(self, keyword: str):
        results = await asyncio.gather(*(self.search(keyword, path=x) for x in self.search_paths))
        merged_results = [item for sublist in results for item in sublist]
        return merged_results


if __name__ == '__main__':
    kkkob = KKKOB()


    async def asyncio_run():
        await kkkob.getToken()
        list = await kkkob.search_batch("庆余年")
        print(json.dumps(list, ensure_ascii=False))


    asyncio.run(asyncio_run())
