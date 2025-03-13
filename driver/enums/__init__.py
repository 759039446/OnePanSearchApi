from enum import Enum
import asyncio
from driver.kkkob import KKKOB



class AsyncEnum(Enum):
    """异步枚举类（类级备注）
    - 功能: 支持动态参数的异步处理模板
    - 版本: v1.2
    """
    ITEM_A = (1,KKKOB.search, "KK大厅", {'token':'7u3j5g3umig', 'endpoint':'http://p.kkkob.com/', 'path':'/v/api/search'})
    ITEM_B = (2,KKKOB.search, "橘子",   {'token':'7u3j5g3umig', 'endpoint':'http://p.kkkob.com/', 'path':'/v/api/search'})

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
        args['token'] = token
        r = await getattr(enum_item, 'function')(**args)
        print(f"执行备注: {enum_item}，{r}")
        # ...原有处理逻辑不变


# 使用示例
async def main():
    result = await AsyncEnum.async_handler(
        AsyncEnum.ITEM_A,
        keyword="庆余年"
    )
    print(result)


asyncio.run(main())
