import yfinance as yf

def fetch_stock_data(symbols):
    stock_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        
        if not stock_info.empty:
            close_price = stock_info["Close"].iloc[-1]
            day_change = stock_info["Close"].pct_change().iloc[-1] * 100
            
            stock_data.append({
                "symbol": symbol,
                "name": stock.info["shortName"],
                "closePrice": close_price,
                "dayChange": day_change
            })
    
    return stock_data
