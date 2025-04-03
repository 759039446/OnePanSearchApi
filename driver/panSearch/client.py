import asyncio

from driver.panSearch.enums import AsyncEnum
from driver.panSearch.kkkob import KKKOB
from driver.panSearch.model.search_result import SearchResult
from driver.common.utils.collection_util import sort_results_by_key


async def search(keyword: str, from_site: list) -> list[SearchResult]:
    print(f"search keyword: {keyword}, from_site: {from_site}")
    enable_enums = AsyncEnum
    if from_site is not None and len(from_site) != 0:
        enable_enums = AsyncEnum.get_enums_by_remark(from_site)
    gg_token, kk_token, xc_token = await asyncio.gather(*[
        KKKOB.getToken("http://gg.ksfuwu.com:8091/", '/api/gettoken'),
        KKKOB.getToken("https://m.kkkba.com/", '/v/api/getToken'),
        KKKOB.getToken("http://xccji.top/", '/v/api/getToken')
    ])
    results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword,
                                                             gg_token=gg_token, kk_token=kk_token, xc_token=xc_token)
                                     for x in enable_enums))
    results = sort_results_by_key(results, "fromSite",
                                  [member.remark for member in sorted(AsyncEnum, key=lambda x: x.num)])
    merged_results = [item for sublist in results for item in sublist]
    return merged_results
