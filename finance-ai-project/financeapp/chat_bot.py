import boto3
import json

bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

user_sessions = {}

def converse_with_claude(user_id: str, message: str, symbol: str):
    conversation = user_sessions.get(user_id, [])
    
    message_with_context = f"{message} (Stock Symbol: {symbol})"
    conversation.append({"role": "user", "content": message_with_context})

    messages_payload = [{"role": msg["role"], "content": [{"text": msg["content"]}]} for msg in conversation]

    try:
        response = bedrock_client.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            body=json.dumps({
                "messages": messages_payload,
                "inferenceConfig": {
                    "maxTokens": 1000,
                    "temperature": 0.5,
                }
            })
        )

        response_content = json.loads(response["body"].read().decode())
        assistant_response = response_content["output"]["message"]["content"][0]["text"]
        conversation.append({"role": "assistant", "content": assistant_response})

        user_sessions[user_id] = conversation

        return {"response": assistant_response, "conversation": conversation}
    
    except Exception as e:
        return {"error": str(e)}