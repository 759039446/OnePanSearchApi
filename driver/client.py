import asyncio

from driver.enums import AsyncEnum
from driver.model.search_result import SearchResult
from utils.collection_util import sort_results_by_key


async def search(keyword: str) -> list[SearchResult]:
    results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword, page='1') for x in AsyncEnum))
    results = sort_results_by_key(results, "from_site", ["KK大厅", "kk短剧", "kk橘子资源", "kk小宇"])
    merged_results = [item for sublist in results for item in sublist]
    return merged_results
