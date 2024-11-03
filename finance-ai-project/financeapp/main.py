import json
from s3_utils import upload_to_s3, download_from_s3
from claude_api import analyze_stock_reports
from stock_data import fetch_stock_data

symbols = [
    "AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "UNH", "JPM", "V",
    "JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
    "CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX"
]

def main():
    stock_symbol = "AAPL"
    result = analyze_stock_reports(stock_symbol)
    # stocks_summary = fetch_stock_data(symbols)
    print(result)


if __name__ == "__main__":
    main()