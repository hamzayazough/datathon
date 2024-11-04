import boto3
import json
import re
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')
bucket_name = "hackathon-storage"


## permet de générer des résumés de rapports financiers pour une entreprise donnée et de les stoquer dans s3 pour y accéder par la suite
## méthode à utiliser seulement lorsqu'un nouveau rapport trimestriel ou annuel est publié
def analyze_stock_reports(stock_symbol):
    s3_key = f"{stock_symbol}_detailed_report.txt"
    
    try:
        existing_file = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        existing_report_summary = existing_file['Body'].read().decode('utf-8')
        return existing_report_summary
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f"No existing report found for {stock_symbol}, generating a new one...")
        else:
            print(f"An unexpected error occurred: {e}")
            return None

    prompt = (
        f"Please review the latest {stock_symbol}-10-K.pdf and {stock_symbol}-10-Q.pdf reports for {stock_symbol} and provide detailed information on the following topics. "
        "If specific information for a topic is not available in the document, omit it from the output.\n\n"
        
        "To ensure accuracy, follow these guidelines:\n"
        "- Search each topic in the most relevant sections of the report, such as 'Management’s Discussion and Analysis,' 'Balance Sheet,' 'Income Statement,' 'Notes to Financial Statements,' and 'Risk Factors.'\n"
        "- Include specific figures, examples, and direct references to sections of the report where relevant.\n\n"
        
        "Topics to Include:\n"
        "1. Number of layoffs: Provide specific numbers and departments affected, if mentioned.\n"
        "2. Executive salaries: List the salaries of top executives and any performance-related bonuses.\n"
        "3. Management changes: Mention recent executive departures, appointments, or restructuring.\n"
        "4. New company acquisitions: Describe any new acquisitions, including purchase price and strategic purpose.\n"
        "5. Restructuring plans: Detail plans for operational or structural changes, with associated costs.\n"
        "6. Performance indicators: Include metrics like revenue growth, profit margins, and ROE.\n"
        "7. Long-term and short-term debt: List debt figures and include maturity dates or interest rates if available.\n"
        "8. Growth objectives: Outline the company's goals for future growth.\n"
        "9. Off-balance sheet commitments: Mention any liabilities not included on the balance sheet.\n"
        "10. Financial forecasts: Include revenue or profit forecasts for the upcoming periods.\n"
        "11. Ongoing litigations: Describe any significant legal cases or regulatory investigations.\n"
        "12. R&D investments: Provide amounts and focus areas.\n"
        "13. Capital expenditures (CapEx): Include budgeted and actual figures for new capital investments.\n"
        "14. Capital structure: Describe the composition of equity, debt, and preferred stock.\n"
        "15. Cash flow: Mention key cash flow indicators from operating, investing, and financing activities.\n"
        "16. Specific risks: List key risks affecting the business, with section references.\n"
        "17. Properties owned: Include major properties or assets owned by the company.\n"
        "18. Dividend policies: Describe current dividend policies, payout ratios, and any recent changes.\n"
        "19. Share buybacks: Mention buyback programs, including quantities and prices if specified.\n"
        "20. Borrowings and financing: Describe new borrowings or financing arrangements.\n"
        "21. Stock holdings by executives: Provide holdings or stock compensation for top executives.\n"
        "22. Compliance expenses: Mention any significant compliance or regulatory costs.\n"
        "23. Potential mergers: Outline any discussions of possible mergers or joint ventures.\n"
        "24. New strategic initiatives: Describe initiatives for expansion, innovation, or new markets.\n"
        "25. Regulatory risks: List risks associated with laws or regulations.\n"
        "26. Market share and segments: Describe the company's market share and major segments.\n"
        "27. Specific ESG indicators: Include environmental, social, and governance metrics.\n"
        "28. Diversity commitments: Outline any diversity or inclusion goals.\n"
        "29. Margin projections: Include projections for gross, operating, or net margins.\n"
        "30. Amortization and depreciation: Mention rates or amounts, particularly if they impact profits.\n"
        "31. Asset impairments: Describe any write-downs or impairments of assets.\n"
        "32. Strategic partnerships: Mention any alliances or collaborations with other companies.\n"
        "33. Workforce variations: Include changes in employee headcount or demographics.\n"
        "34. Competitive advantages: Describe the company's primary competitive strengths.\n"
        "35. Sustainability programs: Mention programs or initiatives focused on sustainability.\n"
        "36. Upcoming products or services: Include details on any new offerings expected soon.\n"
        "37. Governance changes: Describe updates to corporate governance or board composition.\n"
        "38. Cost of goods sold: Include COGS figures and relevant details.\n"
        "39. Cybersecurity risks: Describe risks or incidents related to cybersecurity.\n\n"
        
        "Provide a comprehensive, detailed text summary for each topic as a narrative response without JSON formatting."
    )

    knowledge_base_id = "DSFYOVTZIY"
    model_arn = "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 40000,
        "temperature": 0.5,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = client.retrieve_and_generate(
        input={'text': prompt},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': model_arn,
            }
        }
    )

    response_text = response['output']['text']
    
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=response_text,
        ContentType="text/plain"
    )
    
    return response_text
