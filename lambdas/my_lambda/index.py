import json
import time
import boto3


import boto3


s3Bucket = "learngpt-s3"


def main(event, context):
    start_time = time.time()
    response_body = "No body"
    # http_method = event.get("httpMethod", None)
    http_method = event["httpMethod"]
    client_body = event["body"]
    # http_method = "POST"
    if client_body and http_method:
        if http_method == "POST":
            response_body = generateTextByTitan(client_body)
    end_time = time.time()
    execution_time = "Program Run Time : %.2f sec" % (end_time - start_time)

    return {
        "statusCode": 200,
        "body": "{}\n\n{}".format(execution_time, response_body),
        "headers": {"Content-Type": "text/plain"},
    }


def generateTextByTitan(client_prompt):
    client_bedrock = boto3.client("bedrock-runtime")
    client_s3 = boto3.client("s3")
    input_prompt = """{}""".format(client_prompt)
    response_bedrock = client_bedrock.invoke_model(
        contentType="application/json",
        accept="application/json",
        # modelId="stability.stable-diffusion-xl-v1",
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(
            {
                "max_tokens": 256,
                "messages": [{"role": "user", "content": input_prompt}],
                "anthropic_version": "bedrock-2023-05-31",
            }
        ),
    )
    response_body = json.loads(response_bedrock["body"].read())
    finish_reason = response_body.get("error")
    if finish_reason is not None:
        raise Exception(f"Text generation error. Error is {finish_reason}")
    return response_body["content"][0]["text"]
