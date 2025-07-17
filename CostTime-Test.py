import asyncio
import time

from driver.panSearch.enums import AsyncEnum
from driver.panSearch.kkkob import KKKOB
from driver.panSearch.model.search_result import SearchResult
from driver.common.utils.collection_util import sort_results_by_key


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


async def timed_execution(task, note):
    """包装协程并记录执行时间"""
    start_time = time.time()
    try:
        result = await task
    except Exception as e:
        result = "接口出错"
    finally:
        elapsed = time.time() - start_time
        print(f"{Colors.RED}DEBUG || Task for {note} took {elapsed:.2f}s , result {result}\n", Colors.RESET)
        return result


async def search(keyword: str, from_site: list) -> list[SearchResult]:
    print(f"search keyword: {keyword}, from_site: {from_site}")
    enable_enums = AsyncEnum
    if from_site is not None and len(from_site) != 0:
        enable_enums = AsyncEnum.get_enums_by_remark(from_site)

    # 获取 token 的并行请求（已包含计时）
    gg_token, kk_token, xc_token = await asyncio.gather(*[
        timed_execution(KKKOB.getToken("http://gg.ksfuwu.com:8091/", '/api/gettoken'), "获取ggtoken"),
        timed_execution(KKKOB.getToken("https://m.kkkba.com/", '/v/api/getToken'), "获取kktoken"),
        timed_execution(KKKOB.getToken("http://xccji.top/", '/v/api/getToken'), "获取小草token")
    ])

    # 主搜索任务的并行请求（添加计时）
    search_tasks = [
        timed_execution(AsyncEnum.async_handler(
            x, keyword=keyword,
            gg_token=gg_token, kk_token=kk_token, xc_token=xc_token
        ), x.remark) for x in enable_enums
    ]
    results = await asyncio.gather(*search_tasks)

    results = sort_results_by_key(
        results, "fromSite",
        [member.remark for member in sorted(AsyncEnum, key=lambda x: x.num)]
    )
    merged_results = [item for sublist in results for item in sublist]
    return merged_results


if __name__ == "__main__":
    asyncio.run(timed_execution(search("桃花映江山", None), "全接口搜索"))
