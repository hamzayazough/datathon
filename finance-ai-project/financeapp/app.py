from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI
from stock_data import *
from stock_analysis import *


app = FastAPI()

class NewsItem(BaseModel):
    summary: str
    url: str
    sentiment_score: Optional[float] = None

class StockNewsResponse(BaseModel):
    news: List[NewsItem]

symbols = [
    "AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "MDGL", "JPM", "V",
    "JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
    "CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX"
]

# fonctionnel
@app.get("/stocks")
async def get_stocks():
    try:
        stocks_summary = fetch_stock_data(symbols)
        return stocks_summary
    except Exception as e:
        return {"error": str(e)}

# fonctionnel
@app.get("/stocks/{symbol}/market-cap")
async def get_stock(symbol: str):
    try:
        stock_data = fetch_stock_market_cap(symbol)
        return stock_data
    except Exception as e:
        return {"error": str(e)}

# fonctionnel
@app.get("/stocks/{symbol}/stock-news", response_model=StockNewsResponse)
async def get_stock_news(symbol: str):
    try:
        stock_news = get_filtered_news_for_ticker(symbol, 6)
        print("Durée de l'appel")
        return {"news": stock_news}
    except Exception as e:
        return {"error": str(e)}

# fonctionnel
@app.get("/stocks/{symbol}/sector-news", response_model=StockNewsResponse)
async def get_stock_news(symbol: str):
    try:
        stock_news = get_filtered_news_for_sector(symbol, 6)
        print("Durée de l'appel")
        return {"news": stock_news}
    except Exception as e:
        return {"error": str(e)}
