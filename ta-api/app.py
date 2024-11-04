from fastapi import FastAPI, HTTPException
from stock import *
from fastapi.middleware.cors import CORSMiddleware from

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

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
