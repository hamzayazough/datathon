from fastapi import FastAPI
from stock_data import *

app = FastAPI()

symbols = [
    "AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "BRK.B", "JPM", "V",
    "JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
    "CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX"
]

@app.get("/stocks")
async def get_stocks():
    try:
        stocks_summary = fetch_stock_data(symbols)
        console.log(stocks_summary)
        return stocks_summary
    except Exception as e:
        return {"error": str(e)}

@app.get("/stocks/{symbol}/market-cap")
async def get_stock(symbol: str):
    try:
        stock_data = fetch_stock_market_cap(symbol)
        return stock_data
    except Exception as e:
        return {"error": str(e)}