import json
from claude_api import analyze_stock_reports
from stock_data import *
from stock_analysis import make_news_prompt

symbols = [
    "AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "UNH", "JPM", "V",
    "JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
    "CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX"
]

def main():
    stock_symbol = "AAPL"
    # result = fetch_stock_market_cap(stock_symbol)
    # stocks_summary = fetch_stock_data(symbols)
    result  = make_news_prompt(stock_symbol, 5)
    print(result)


if __name__ == "__main__":
    main()