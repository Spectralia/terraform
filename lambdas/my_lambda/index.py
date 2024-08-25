import json
import boto3

# import time


def main(event, context):
    response_body = listAvailableModels(event, context)
    return {"status": 200, "body": json.dumps(response_body)}


def listAvailableModels(event, context):
    client_bedrock = boto3.client("bedrock")
    response = client_bedrock.list_foundation_models()
    response_body = []
    for summary in response["modelSummaries"]:
        response_body.append({summary["providerName:"]: summary["modelId"]})
    return response_body
