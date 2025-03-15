from fastapi import FastAPI, Query
from driver.client import search
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search")
async def search_pan(
    keyword: str = Query(..., description="必填查询参数"),
    type: str = Query(None, description="可选网盘类型"),
    fromSite: list = Query(None, description="可选来源站点", style="form", explode=False)
):
    results = await search(keyword, fromSite)
    filtered_results = [
        res
        for res in results
        if (not type or res['type'] == type)
    ]
    return {'success':True,'data':filtered_results,'message':"搜索成功",'code':200}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=21123)