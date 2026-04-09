import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_request(url, params=None):
    try:
        resp = requests.get(url, params=params, timeout=10, verify=False)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return {"value": []}

@app.get("/api/ssq")
def get_ssq_37():
    data = safe_request("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=200&provinceId=0&pageSize=37")
    history = []
    for item in data.get("value", []):
        try:
            red = list(map(int, item["lotteryDrawResult"].split("|")[0].split(",")))
            blue = list(map(int, item["lotteryDrawResult"].split("|")[1].split(",")))
            history.append({"red": red, "blue": blue})
        except:
            continue
    return history

@app.get("/api/dlt")
def get_dlt_37():
    data = safe_request("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=800&provinceId=0&pageSize=37")
    history = []
    for item in data.get("value", []):
        try:
            red = list(map(int, item["lotteryDrawResult"].split("|")[0].split(",")))
            blue = list(map(int, item["lotteryDrawResult"].split("|")[1].split(",")))
            history.append({"red": red, "blue": blue})
        except:
            continue
    return history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)