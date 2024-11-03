import boto3
import json
import requests
from config import ALPHAVANTAGE_ACCESS_KEY

client = boto3.client('bedrock-runtime', region_name='us-west-2')

def fetch_from_alphavantage(endpoint: str, params: dict):
    base_url = "https://www.alphavantage.co/query"
    params["apikey"] = ALPHAVANTAGE_ACCESS_KEY
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data from Alphavantage:", response.status_code)
        return {}

def get_sectors_for_ticker(ticker: str):
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
    }
    data = fetch_from_alphavantage("OVERVIEW", params)
    return data.get("Sector", "Unknown") if data else "Unknown"

def fetch_news(ticker: str = None, sector: str = None, max_articles: int = 100):
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": max_articles
    }
    if sector:
        params["topic"] = sector
        params.pop("tickers", None)
    news_data = fetch_from_alphavantage("NEWS_SENTIMENT", params)
    news_list = news_data.get("feed", [])
    
    filtered_news = []
    for item in news_list:
        ticker_sentiment = item.get("ticker_sentiment", [])
        
        for sentiment in ticker_sentiment:
            if ticker and sentiment["ticker"] == ticker and float(sentiment["relevance_score"]) > 0.5:
                filtered_news.append({
                    "summary": item.get("summary", ""),
                    "url": item.get("url", ""),
                    "sentiment_score": float(sentiment.get("ticker_sentiment_score", 0))
                })
                break
            elif sector and float(sentiment["relevance_score"]) > 0.2:
                filtered_news.append({
                    "summary": item.get("summary", ""),
                    "url": item.get("url", ""),
                    "sentiment_score": float(sentiment.get("ticker_sentiment_score", 0))
                })
                break

    return filtered_news

def send_to_claude(prompt, retries=3):
    for attempt in range(retries):
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        
        raw_response = response['body'].read()
        print("Raw Response:", raw_response)
        
        try:
            response_body = json.loads(raw_response)
            response_text = response_body.get("content", [{}])[0].get("text", "")
            
            try:
                response_json = json.loads(response_text)
                return response_json
            except json.JSONDecodeError:
                print(f"Attempt {attempt + 1}: Response text is not valid JSON. Retrying...")

        except Exception as e:
            print("Error processing response:", e)
            return {"error": "Response processing error"}

    print("Error: Response is not valid JSON after multiple attempts.")
    return {"error": "Response is not valid JSON"}

def make_news_prompt(news, ticker_or_sector: str, max_results: int):
    news_resumes = [(i, x["summary"], x["sentiment_score"]) for i, x in enumerate(news[:max_results])]

    prompt = f"""
    You are a bot helping financial analysts. Out of the following {max_results} news summaries, please select the ones that are most pertinent for evaluating: {ticker_or_sector}.
    Return the answer as a JSON array. Each element should include:
    - "description" with a summary of the news article,
    - "sentiment" which is the provided sentiment score,
    - "index" for the position of the article.

    Format each JSON object strictly as:
    [
        {{"description": "summary of the news article", "sentiment": sentiment_score, "index": "index number"}},
        ...
    ]
    Here are the article summaries with sentiment scores: {news_resumes}
    """

    return send_to_claude(prompt)

def get_filtered_news_for_ticker(ticker: str, max_results: int):
    news = fetch_news(ticker=ticker)
    return make_news_prompt(news, ticker, max_results)

def get_filtered_news_for_sector(sector: str, max_results: int):
    news = fetch_news(sector=sector)
    return make_news_prompt(news, sector, max_results)
