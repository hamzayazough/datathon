from fastapi import FastAPI, HTTPException
from stock import *


app = FastAPI()

@app.get('/historic/')
async def historic(ticker:  str = '', period: str = '1y'):
    data = await getHistory(ticker,period)
    if data == None:
        raise HTTPException(status_code=400)
    return json.loads(data)

@app.get('/indicator/')
def indicator(ticker:str = '', period: str = '1y', indicator: str = ''):
    data = calculateIndicator(ticker, period, indicator)
    if data == None:
        raise HTTPException(status_code=400)
    return json.loads(data)