from driver.kkkob.main import KKKOB

kkkob = KKKOB()


async def search(keyword: str):
    return await kkkob.search_batch(keyword)
