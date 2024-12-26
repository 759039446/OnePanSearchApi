from fastapi import FastAPI
from driver.client import search
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search/{keyword}")
async def search_pan(keyword: str):
    res = await search(keyword)
    return {'success':True,'data':res,'message':"搜索成功",'code':200}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=21123)