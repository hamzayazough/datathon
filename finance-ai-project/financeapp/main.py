import json
from reports_analysis import analyze_stock_reports
from stock_data import *
from stock_analysis import *

symbols = [
    "AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "UNH", "JPM", "V",
    "JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
    "CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX"
]

def main():
    stock_symbol = "MSFT"
    result  = analyze_stock_reports(stock_symbol)
    print(result)
    

if __name__ == "__main__":
    main()