import boto3

client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')
messages = []

def chat(msg):
    messages.append({"text": msg})
    res = client.converse(modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[{"role": "user", "content": messages}],
        )
    messages.append(res['output']['message']['content'][-1])
    return res['output']['message']['content']

