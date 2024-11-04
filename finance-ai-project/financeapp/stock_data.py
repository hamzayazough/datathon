import yfinance as yf 
from math import isnan, isinf

def sanitize_value(value):
    if isnan(value) or isinf(value):
        return None
    return value

def fetch_stock_data(symbols):
    stock_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d", interval="1h")
        if not stock_info.empty:
            close_price = sanitize_value(stock_info["Close"].iloc[-1])
            day_change = sanitize_value(stock_info["Close"].pct_change().sum() * 100)
            
            stock_data.append({
                "symbol": symbol,
                "name": stock.info.get("shortName", "Unknown"),
                "closePrice": close_price,
                "dayChange": day_change
            })
    
    return stock_data


def fetch_stock_market_cap(symbol):
    stock = yf.Ticker(symbol)
    stock_info = stock.info

    stock_data = {
        "symbol": symbol,
        "name": stock_info.get("shortName", "N/A"),
        "sector": stock_info.get("sector", "N/A"),
        "industry": stock_info.get("industry", "N/A"),
        "marketCap": stock_info.get("marketCap", "N/A"),
        "volume": stock_info.get("volume", "N/A"),
        "peRatio": stock_info.get("trailingPE", "N/A"),
        "forwardPE": stock_info.get("forwardPE", "N/A"),
        "dividendYield": stock_info.get("dividendYield", "N/A"),
        "dividendRate": stock_info.get("dividendRate", "N/A"),
        "dividendPayDate": stock_info.get("exDividendDate", "N/A"),
        "beta": stock_info.get("beta", "N/A"),
        "eps": stock_info.get("trailingEps", "N/A"),
        "52WeekHigh": stock_info.get("fiftyTwoWeekHigh", "N/A"),
        "52WeekLow": stock_info.get("fiftyTwoWeekLow", "N/A"),
        "priceToBook": stock_info.get("priceToBook", "N/A"),
    }

    return stock_data