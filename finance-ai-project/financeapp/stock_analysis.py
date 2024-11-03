import boto3
import json
import requests
from config import ALPHAVANTAGE_ACCESS_KEY

client = boto3.client('bedrock-runtime', region_name='us-west-2')
def fetch_news_from_alphavantage(ticker: str):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHAVANTAGE_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        news_list = news_data.get("feed", [])
        
        filtered_news = []
        for item in news_list:
            ticker_sentiment = item.get("ticker_sentiment", [])
            
            for sentiment in ticker_sentiment:
                if sentiment["ticker"] == ticker and float(sentiment["relevance_score"]) > 0.5:
                    filtered_news.append({
                        "summary": item.get("summary", ""),
                        "url": item.get("url", "")
                    })
                    break

        return filtered_news
    else:
        print("Error fetching news:", response.status_code)
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
        print("Raw Response:", raw_response)
        
        try:
            response_body = json.loads(raw_response)
            response_text = response_body.get("content", [{}])[0].get("text", "")
            
            # Essayez de charger la réponse textuelle comme JSON
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

def make_news_prompt(ticker: str, k: int):
    news = fetch_news_from_alphavantage(ticker)
    news_resumes = [(i, x["summary"]) for i, x in enumerate(news[:k])]

    prompt = f"""
    You are a bot helping financial analysts. Out of the following {k} news summaries, please select the ones that are most pertinent for evaluating the stock: {ticker}.
    Return the answer as a JSON array. Each element should include:
    - "description" with a summary of the news article,
    - "sentiment" as an integer (1 for positive, -1 for negative, 0 for neutral),
    - "index" for the position of the article.

    Format each JSON object strictly as:
    [
        {{"description": "summary of the news article", "sentiment": 1, "index": "index number"}},
        ...
    ]
    Make sure the response is a well-formed JSON array with all keys and values in double quotes. Here are the article summaries: {news_resumes}
    """

    res = send_to_claude(prompt)
    pertinent_news = []

    if isinstance(res, list):
        try:
            pertinent_news = [
                {
                    "description": item["description"],
                    "index": int(item["index"]),
                    "sentiment": int(item.get("sentiment", 0))  # Définit 0 si "sentiment" est absent
                }
                for item in res
                if "description" in item and "index" in item and str(item["index"]).isdigit()
            ]
        except (ValueError, TypeError, KeyError) as e:
            print("Formatting error:", e)
            pertinent_news = []
    else:
        print("Error in Claude response:", res.get("error", "Unknown error"))

    final_news = [news[item["index"]] for item in pertinent_news if item["index"] < len(news)]
    return final_news[:k]
