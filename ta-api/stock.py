import yfinance as yf
import json
import numpy as np
from talib import abstract



async def getHistory(ticker: str, period: str):
    ticker =  yf.Ticker(ticker)
    if ticker == None:
        return None
    data = ticker.history(period=period)
    if data.empty:
        return None
    return data.to_json()

def calculateIndicator(ticker: str, period: str, indicator: str):
    ticker = yf.Ticker(ticker)
    data = ticker.history(period=period)
    data.columns = data.columns.str.lower()
    function = abstract.Function(indicator)
    if (ticker == None):
        return None
    return function(data).to_json()