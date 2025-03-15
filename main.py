from fastapi import FastAPI, Query
from driver.client import search

app = FastAPI(title="PanFileSearch API",
    description="网盘文件搜索服务",
    version="2.0.0")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
async def search_pan(
        keyword: str = Query(..., description="必填查询参数"),
        type: str = Query(None, description="可选网盘类型"),
        fromSite: list = Query(None, description="可选来源站点", style="form", explode=False),
        page: int = Query(1, ge=1, description="页码，从1开始"),
        pageSize: int = Query(10, ge=1, description="每页数量")
):
    results = await search(keyword, fromSite)
    filtered_results = [
        res
        for res in results
        if (not type or res['type'] == type)
    ]
    total = len(filtered_results)
    start = (page - 1) * pageSize
    end = page * pageSize
    paged_results = filtered_results[start:end]

    return {
        'success': True,
        'data': paged_results,
        'total': total,
        'message': "搜索成功",
        'code': 200
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=21123)