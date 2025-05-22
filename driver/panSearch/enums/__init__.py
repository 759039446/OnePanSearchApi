from enum import Enum
import asyncio
from typing import List

from driver.panSearch.pansearch import PanSearch
from driver.panSearch.tempalte import Template, FUN_PAN, GET_API, GET_API_2, GET_API_3
from driver.panSearch.kkkob import KKKOB
from driver.common.utils.collection_util import sort_results_by_key
from driver.common.utils.dict_formatter_util import format_dict


class AsyncEnum(Enum):
    """异步枚举类（类级备注）
    - 功能: 支持动态参数的异步处理模板
    - 版本: v1.2
    """
    ITEM_PAN_SEARCH = (
        0, PanSearch.search, "PanSearch",
        {'keyword': '{keyword}', 'endpoint': 'https://www.pansearch.me/','path': '/search'})
    ITEM_A_1 = (
        9999, KKKOB.search, "kk大厅",
        {'keyword': '{keyword}', 'token': '{gg_token}', 'endpoint': 'http://gg.ksfuwu.com:8091/', 'path': '/api/sortWeb',
         'userid': '191201nf'})
    ITEM_A_2 = (
        9998, KKKOB.search, "kk大厅",
        {'keyword': '{keyword}', 'token': '{gg_token}', 'endpoint': 'http://gg.ksfuwu.com:8091/',
         'path': '/api/sortWeb',
         'userid': '201211nf'})
    ITEM_A_3 = (
        9997, KKKOB.search, "kk大厅",
        {'keyword': '{keyword}', 'token': '{gg_token}', 'endpoint': 'http://gg.ksfuwu.com:8091/',
         'path': '/api/sortWeb',
         'userid': '201212nf'})
    ITEM_A_4 = (
        9996, KKKOB.search, "kk大厅",
        {'keyword': '{keyword}', 'token': '{xc_token}', 'endpoint': 'http://xccji.top/',
         'path': '/v/api/sortWeb',
         'userid': '200317xlb'})
    ITEM_KK_1 = (
        10, KKKOB.search, "kk短剧",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://m.kkkba.com/', 'path': '/v/api/getDJ'})
    ITEM_KK_2 = (
        11, KKKOB.search, "kk橘子资源",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://m.kkkba.com/', 'path': '/v/api/getJuzi'})
    ITEM_KK_3 = (
        11, KKKOB.search, "kk小宇",
        {'keyword': '{keyword}', 'token': '{kk_token}', 'endpoint': 'https://m.kkkba.com/', 'path': '/v/api/getXiaoyu'})
    ITEM_B = (
        40, KKKOB.search, "kk小悠",
        {'keyword': '{keyword}', 'token': '{gg_token}', 'endpoint': 'http://gg.ksfuwu.com:8091/', 'path': '/api/getXiaoy'})
    ITEM_D = (
        60, KKKOB.search, "kk天天追剧",
        {'keyword': '{keyword}', 'token': '{gg_token}', 'endpoint': 'http://gg.ksfuwu.com:8091/', 'path': '/api/getTTZJB'})
    ITEM_DYFX = (
        61, KKKOB.search, "kk短剧2",
        {'keyword': '{keyword}', 'token': '{xc_token}', 'endpoint': 'http://xccji.top/', 'path': '/v/api/getDyfx'})

    ITEM_E = (
        99999, Template.search, "趣盘搜",
        {'keyword': '{keyword}', 'endpoint': 'https://v.funletu.com', 'path': '/search', 'temp_name': FUN_PAN,
         'id_field': 'id', 'title_field': 'title', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_F = (
        800, Template.search, "酷乐—百度",
        {'keyword': '{keyword}', 'endpoint': 'https://api.kuleu.com/', 'path': '/api/bddj?text=', 'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'viewlink', 'pwd_field': 'extcode'})
    ITEM_G = (
        900, Template.search, "酷乐—夸克",
        {'keyword': '{keyword}', 'endpoint': 'https://api.kuleu.com/', 'path': '/api/action?text=', 'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'viewlink', 'pwd_field': 'extcode'})

    ITEM_AI_KAN = (
        1010, Template.search, "爱看短剧",
        {'keyword': '{keyword}', 'endpoint': 'https://ys.110t.cn/', 'path': '/api/ajax.php?act=search&name=',
         'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_ycubbs = (
        1020, Template.search, "ycubbs",
        {'keyword': '{keyword}', 'endpoint': 'https://ai-img.ycubbs.cn/', 'path': '/api/duanju/search?name=',
         'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_MENGQIANYU = (
        1030, Template.search, "梦牵云",
        {'keyword': '{keyword}', 'endpoint': 'https://api.qsdurl.cn/', 'path': '/tool/duanju/?name=',
         'temp_name': GET_API_2,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_LONGZHU_DJ = (
        1040, Template.search, "龙珠-短剧",
        {'keyword': '{keyword}', 'endpoint': 'https://api.dragonlongzhu.cn/', 'path': '/api/duanju_cat.php?name=',
         'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'title', 'url_field': 'url', 'pwd_field': 'extcode'})
    # ITEM_LONGZHU_YS = (
    #     1040, Template.search, "龙珠-影视",
    #     {'keyword': '{keyword}', 'endpoint': 'https://api.dragonlongzhu.cn/', 'path': '/api/ziyuan_nanfeng.php?keysearch=',
    #      'temp_name': GET_API,
    #      'id_field': 'id', 'title_field': 'title', 'url_field': 'data_url', 'pwd_field': 'extcode'})
    ITEM_6789o_1 = (
        1050, Template.search, "6789o",
        {'keyword': '{keyword}', 'endpoint': 'https://zy.6789o.com/', 'path': '/duanjuapi/search.php?text=',
         'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'viewlink', 'pwd_field': 'extcode'})
    ITEM_6789o_2 = (
        1051, Template.search, "6789o",
        {'keyword': '{keyword}', 'endpoint': 'https://www.6789o.com/', 'path': '/api/duanju_apihj.php?name=',
         'temp_name': GET_API,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'url', 'pwd_field': 'extcode'})
    ITEM_6789o_3 = (
        1052, Template.search, "6789o",
        {'keyword': '{keyword}', 'endpoint': 'https://www.6789o.com/', 'path': '/api/baiduziyuan_apiheji.php?name=',
         'temp_name': GET_API_3,
         'id_field': 'id', 'title_field': 'name', 'url_field': 'url', 'pwd_field': 'extcode'})

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

        # 构建 remark到枚举列表的映射
        remark_map = {}
        for member in cls:
            if member.remark not in remark_map:
                remark_map[member.remark] = []
            remark_map[member.remark].append(member)

        # 收集所有匹配的枚举成员
        result = []
        for remark in remarks:
            if remark in remark_map:
                result.extend(remark_map[remark])

        return result
    @staticmethod
    async def async_handler(enum_item: Enum, **kwargs):
        """异步核心方法（方法级备注）
        Args:
            enum_item: 必须传入本枚举成员
            **kwargs: 动态关键字参数
        """

        # 合并默认参数和动态参数
        args = getattr(enum_item, 'args').copy()
        args.update(**kwargs)
        args = format_dict(args, {
                                    'gg_token': kwargs.get('gg_token'),
                                    'kk_token': kwargs.get('kk_token'),
                                    'xc_token': kwargs.get('xc_token')})
        return await getattr(enum_item, 'function')(**args, from_site=getattr(enum_item, 'remark'))


if __name__ == '__main__':
    # 使用示例
    async def main():
        keyword = "重生"
        results = await asyncio.gather(*(AsyncEnum.async_handler(x, keyword=keyword, page='1') for x in AsyncEnum))
        results = sort_results_by_key(results, "from_site", [member.remark for member in sorted(AsyncEnum, key=lambda x: x.num)])
        merged_results = [item for sublist in results for item in sublist]

        print(merged_results)


    asyncio.run(main())
