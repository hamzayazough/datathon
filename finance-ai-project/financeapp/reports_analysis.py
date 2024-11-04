import boto3
import json
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
client = boto3.client('bedrock-runtime', region_name='us-west-2')
bucket_name = "hackathon-storage"

def analyze_stock_reports(stock_symbol):
    s3_key = f"{stock_symbol}_detailed_report.txt"

    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_key)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return []
        else:
            print(f"Erreur lors de la vérification du fichier S3 : {e}")
            return []

    try:
        file_object = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        file_content = file_object['Body'].read().decode()

        prompt = (
            "Human: Extract key financial analysis elements from the following document. "
            "Return a JSON array containing between 5 and 7 key elements that a financial analyst would find critical for understanding this report. "
            f"Each item should have 'element' with a summary, and 'source' set to '{stock_symbol}_10_K_2024'."
            f"\n\nDocument Content:\n{file_content}"
        )

        input_data = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            body=json.dumps(input_data)
        )

        response_content = response["body"].read().decode()

        try:
            assistant_text = json.loads(response_content)["content"][0]["text"]

            start = assistant_text.find('[')
            end = assistant_text.rfind(']') + 1
            json_content = assistant_text[start:end]

            important_elements = json.loads(json_content)


            return important_elements

        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Erreur lors de l'extraction ou du parsing du JSON : {e}")
            return []

    except ClientError as e:
        print(f"Erreur lors de l'appel de l'endpoint : {e}")
        return []
