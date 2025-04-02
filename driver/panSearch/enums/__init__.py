from enum import Enum
import asyncio
from typing import List

from driver.panSearch.tempalte import Template, FUN_PAN, GET_API
from driver.panSearch.kkkob import KKKOB
from driver.common.utils.collection_util import sort_results_by_key
from driver.common.utils.dict_formatter_util import format_dict


class AsyncEnum(Enum):
    """异步枚举类（类级备注）
    - 功能: 支持动态参数的异步处理模板
    - 版本: v1.2
    """
    ITEM_A = (
        1, KKKOB.search, "kk大厅",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://s.kkkba.com/', 'path': '/v/api/search'})
    ITEM_B = (
        2, KKKOB.search, "kk短剧",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://s.kkkba.com/', 'path': '/v/api/getDJ'})
    ITEM_C = (
        3, KKKOB.search, "kk橘子资源",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://s.kkkba.com/', 'path': '/v/api/getJuzi'})
    ITEM_D = (
        4, KKKOB.search, "kk小宇",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://s.kkkba.com/', 'path': '/v/api/getXiaoyu'})

    ITEM_E = (
        5, Template.search, "趣盘搜",
        {'keyword': '{keyword}', 'endpoint': 'https://v.funletu.com', 'path': '/search', 'temp_name': FUN_PAN,
         'id_field': 'id', 'title_field': 'title', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_F = (
        6, Template.search, "酷乐—百度",
        {'keyword': '{keyword}', 'endpoint': 'https://api.kuleu.com/', 'path': '/api/bddj?text=', 'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'viewlink', 'pwd_field': 'extcode'})
    ITEM_G = (
        7, Template.search, "酷乐—夸克",
        {'keyword': '{keyword}', 'endpoint': 'https://api.kuleu.com/', 'path': '/api/action?text=', 'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'viewlink', 'pwd_field': 'extcode'})

    def __init__(self, num, function, remark, args: dict):
        self.num = num
        self.function = function
        self.remark = remark  # 成员级备注属性
        self.args = args

    @classmethod
    def get_enums_by_remark(cls, remarks: list) -> List['AsyncEnum']:
        """
        根据remark数组筛选枚举成员
        Args:
            remarks: 需要匹配的remark列表
        Returns:
            匹配成功的枚举成员列表（按输入顺序）
        """
        if not remarks:
            return []

        # 构建 remark到枚举的映射
        remark_map = {member.remark: member for member in cls}
        return [remark_map[remark] for remark in remarks if remark in remark_map]

    @staticmethod
    async def async_handler(enum_item: Enum, **kwargs):
        """异步核心方法（方法级备注）
        Args:
            enum_item: 必须传入本枚举成员
            **kwargs: 动态关键字参数
        """
        token = await KKKOB.getToken("https://s.kkkba.com/")
        # 合并默认参数和动态参数
        args = getattr(enum_item, 'args').copy()
        args.update(**kwargs)
        args = format_dict(args, {'kk_token': token})
        return await getattr(enum_item, 'function')(**args, from_site=getattr(enum_item, 'remark'))


if __name__ == '__main__':
    # 使用示例
    async def main():
        keyword = "重生"
        results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword, page='1') for x in AsyncEnum))
        results = sort_results_by_key(results, "from_site", ["KK大厅", "kk短剧", "kk橘子资源", "kk小宇", "趣盘搜",
                                                             "酷乐—百度","酷乐—夸克"])
        merged_results = [item for sublist in results for item in sublist]

        print(merged_results)


    asyncio.run(main())
