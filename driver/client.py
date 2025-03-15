import asyncio

from driver.enums import AsyncEnum
from driver.model.search_result import SearchResult
from utils.collection_util import sort_results_by_key


async def search(keyword: str, from_site: list) -> list[SearchResult]:
    enable_enums = AsyncEnum
    if from_site is not None:
        enable_enums = AsyncEnum.get_enums_by_remark(from_site)
    results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword) for x in enable_enums))
    results = sort_results_by_key(results, "fromSite",
                                  [AsyncEnum.ITEM_A.remark, AsyncEnum.ITEM_B.remark,
                                   AsyncEnum.ITEM_C.remark, AsyncEnum.ITEM_D.remark])
    merged_results = [item for sublist in results for item in sublist]
    return merged_results