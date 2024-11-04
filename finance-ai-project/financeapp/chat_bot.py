import boto3
import json

bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

user_sessions = {}

def converse_with_claude(message: str, symbol: str):
    print(f"Conversing with Claude for symbol {symbol} with message: {message}")
    
    conversation = user_sessions.get(symbol, [])
    
    message_with_context = f"{message} (Stock Symbol: {symbol})"
    conversation.append({"role": "user", "content": message_with_context})

    messages_payload = [{"role": msg["role"], "content": [{"text": msg["content"]}]} for msg in conversation]

    try:
        response = bedrock_client.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            messages=messages_payload,
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.5,
            }
        )

        response_content = response["output"]["message"]["content"][0]["text"]
        conversation.append({"role": "assistant", "content": response_content})

        user_sessions[symbol] = conversation

        return {"response": response_content}
    
    except Exception as e:
        return {"error": str(e)}