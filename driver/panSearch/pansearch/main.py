import asyncio
import re
import traceback
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from driver.common.utils.pan_type_util import get_pan_type
from driver.panSearch.model.search_result import SearchResult


async def aio_request(method: str, url: str, **kwargs) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            return await response.text()


class PanSearch:

    @staticmethod
    async def search(keyword, endpoint, path,pan='', offset=0, **keywords) -> list[SearchResult]:
        results = []
        params = {
            'keyword': keyword,
            'pan': pan,
            'offset': offset
        }
        url = urljoin(endpoint, path)
        try:
            # url = f'https://www.pansearch.me/search'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
            content = await aio_request('GET', url, headers=headers,params=params,
                                        timeout=aiohttp.ClientTimeout(total=30), ssl=False)
            soup = BeautifulSoup(content, 'lxml')
            nodes = soup.select('.whitespace-pre-wrap.break-all')

            for node in nodes:
                content = node.get_text()
                title_match = re.search(r'名称：(.*?)\n\n描述：', content)
                url_match = re.search(r'链接：(https://pan\.quark\.cn/s/[a-zA-Z0-9]+)', content)

                if title_match and url_match:
                    url = url_match.group(1)
                    name = title_match.group(1).strip()
                    results.append(SearchResult(
                        id='',
                        name=name.replace('<em>', '').replace('</em>', ''),
                        url=url,
                        type=get_pan_type(url),
                        pwd='',
                        fromSite=keywords.get('from_site', ''),
                        code="0"
                    ))
                if len(results) >= 14:
                    break  # 根据页面配置动态决定

        except aiohttp.ClientConnectorError as e:
            print(f"ERROR || panSearch请求失败 || {e}")
        except asyncio.TimeoutError as e:
            print(f"ERROR || panSearch请求超时 || {e}")
        except Exception as e:
            traceback.print_exc()
            print(f"ERROR || panSearch错误 || {e}")
        return results
