import boto3
import json
import requests
import yfinance as yf
from textblob import TextBlob
from datetime import datetime, timedelta
from config import FINNHUB_API_KEY
from pydantic import BaseModel, ValidationError
from typing import List

class NewsItemModel(BaseModel):
    summary: str
    url: str

class ClaudeResponseModel(BaseModel):
    items: List[NewsItemModel] 

client = boto3.client('bedrock-runtime', region_name='us-west-2')


def get_sectors_for_ticker(ticker: str):
    """Obtenir le secteur d'un ticker spécifique en utilisant yfinance."""
    try:
        stock = yf.Ticker(ticker)
        sector = stock.info.get("sector", "Unknown")
        return sector if sector else "Unknown"
    except Exception as e:
        print(f"Erreur lors de la récupération du secteur pour {ticker}: {e}")
        return "Unknown"

def fetch_sector_news(category="general"):
    url = f"https://finnhub.io/api/v1/news?category={category}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        
        filtered_news = [{"summary": item["summary"], "url": item["url"]} for item in news_data if "summary" in item and "url" in item]
        
        return filtered_news
    else:
        print("Erreur lors de la récupération des nouvelles:", response.status_code)
        return []

def fetch_stock_news(ticker: str, max_articles: int = 20):
    base_url = "https://finnhub.io/api/v1/company-news"
    
    today = datetime.now().date()
    five_days_ago = today - timedelta(days=5)
    params = {
        "symbol": ticker,
        "from": five_days_ago.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d"),
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        news_data = response.json()

        filtered_news = [
            {"summary": article["summary"], "url": article["url"]}
            for article in news_data[:max_articles]
            if "summary" in article and "url" in article
        ]
        
        return filtered_news

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news for ticker {ticker}: {e}")
        return []



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

        try:
            response_body = json.loads(raw_response)
            response_text = response_body.get("content", [{}])[0].get("text", "")

            json_start = response_text.find('[')
            if json_start != -1:
                response_text = response_text[json_start:]

            response_json = json.loads(response_text)
            validated_response = ClaudeResponseModel(items=response_json)
            return validated_response.items

        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1}: Response text is not valid JSON. Retrying...")
        except ValidationError as e:
            print("Validation error:", e)
            return {"error": "Invalid response format"}
        except Exception as e:
            print("Error processing response:", e)
            return {"error": "Response processing error"}

    print("Error: Response is not valid JSON after multiple attempts.")
    return {"error": "Response is not valid JSON"}



def make_news_prompt(news, ticker_or_sector: str, max_results: int):
    news_resumes = [{"summary": x["summary"], "url": x["url"]} for x in news[:max_results]]

    prompt = f"""
    Please respond with only a JSON array of the {max_results} most pertinent news summaries for evaluating: {ticker_or_sector}.
    Each JSON object in the array should include:
    - "summary" with a summary of the news article
    - "url" for the article's link

    Example response format:
    [
        {{"summary": "summary of the news article", "url": "link to article"}},
        ...
    ]

    Here are the article summaries: {news_resumes}
    """

    response = send_to_claude(prompt)

    if isinstance(response, list):
        response_with_sentiment = []
        for item in response:
            sentiment_score = TextBlob(item.summary).sentiment.polarity
            response_with_sentiment.append({
                "summary": item.summary,
                "url": item.url,
                "sentiment": sentiment_score
            })
        return response_with_sentiment

    return response



def get_filtered_news_for_ticker(ticker: str, max_results: int):
    news = fetch_stock_news(ticker=ticker)
    return make_news_prompt(news, ticker, max_results)

def get_filtered_news_for_sector(sector: str, max_results: int):
    news = fetch_sector_news(sector)
    return make_news_prompt(news, sector, max_results)
