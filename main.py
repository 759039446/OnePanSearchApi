from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from driver.client import search

app = FastAPI(title="PanFileSearch API",
              description="网盘文件搜索服务",
              version="2.0.0")

# 添加 CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源列表（生产环境需指定具体域名，如 ["http://example.com"]）
    allow_credentials=True,  # 允许携带凭证（如 Cookies）
    allow_methods=["*"],  # 允许的 HTTP 方法（如 ["GET", "POST"]）
    allow_headers=["*"],  # 允许的请求头
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class SourceQuery(BaseModel):
    keyword: str
    fromSite: Optional[List[str]] = None
    type: Optional[str] = None
    page: int = 1
    pageSize: int = 10

    @classmethod
    def from_query(cls,
                   keyword: str = Query(..., description="必填查询参数"),
                   type: str = Query(None, description="可选网盘类型"),
                   fromSite: str = Query(None, description="可选来源站点", explode=False),
                   page: int = Query(1, ge=1, description="页码，从1开始"),
                   pageSize: int = Query(10, ge=1, description="每页数量")):
        if not fromSite:
            return cls(fromSite=None, type=type, keyword=keyword, page=page, pageSize=pageSize)
        # 拆分并验证
        return cls(fromSite=[s.strip() for s in fromSite.split(",")],
                   type=type, keyword=keyword, page=page, pageSize=pageSize)


@app.get("/search")
async def search_pan(
        source: SourceQuery = Depends(SourceQuery.from_query)
):
    print(source)
    results = await search(source.keyword, source.fromSite)
    filtered_results = [
        res
        for res in results
        if (not type or res['type'] == type)
    ]
    total = len(filtered_results)
    start = (source.page - 1) * source.pageSize
    end = source.page * source.pageSize
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
