from enum import Enum
import asyncio
from driver.kkkob import KKKOB
from utils.collection_util import sort_results_by_key
from utils.dict_formatter_util import format_dict


class AsyncEnum(Enum):
    """异步枚举类（类级备注）
    - 功能: 支持动态参数的异步处理模板
    - 版本: v1.2
    """
    ITEM_A = (
        1, KKKOB.search, "KK大厅",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'http://p.kkkob.com/', 'path': '/v/api/search'})
    ITEM_B = (
        2, KKKOB.search, "kk短剧",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'http://p.kkkob.com/', 'path': '/v/api/getDJ'})
    ITEM_C = (
        3, KKKOB.search, "kk橘子资源",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'http://p.kkkob.com/', 'path': '/v/api/getJuzi'})
    ITEM_D = (
        4, KKKOB.search, "kk小宇",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'http://p.kkkob.com/', 'path': '/v/api/getXiaoyu'})

    # ITEM_E = (
    #     5, KKKOB.search, "kk小宇",{'keyword':'{keyword}','token': '{token}', 'endpoint': 'http://p.kkkob.com/', 'path': '/v/api/getSearchX'})

    def __init__(self, num, function, remark, args: dict):
        self.num = num
        self.function = function
        self.remark = remark  # 成员级备注属性
        self.args = args

    @staticmethod
    async def async_handler(enum_item: Enum, **kwargs):
        """异步核心方法（方法级备注）
        Args:
            enum_item: 必须传入本枚举成员
            **kwargs: 动态关键字参数
        """
        token = await KKKOB.getToken("http://p.kkkob.com/")
        # 合并默认参数和动态参数
        args = getattr(enum_item, 'args').copy()
        args.update(**kwargs)
        args = format_dict(args, {'kk_token': token})
        return await getattr(enum_item, 'function')(**args,from_site=getattr(enum_item, 'remark'))


if __name__ == '__main__':
    # 使用示例
    async def main():
        keyword = "重生"
        results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword, page='1') for x in AsyncEnum))
        results = sort_results_by_key(results, "from_site", ["KK大厅", "kk短剧", "kk橘子资源", "kk小宇"])
        merged_results = [item for sublist in results for item in sublist]

        print(merged_results)


    asyncio.run(main())
