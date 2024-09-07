import json
import time
import boto3
import base64
import datetime
import random

import boto3

# import time

s3Bucket = "learngpt-s3"
# t_delta = datetime.timedelta(hours=-8)
# PST = datetime.timezone(t_delta, "PST")
# now = datetime.datetime(PST)
fileNum = random.randint(0, 4294967295)


def main(event, context):
    start_time = time.time()
    response_body = "No body"
    # http_method = event.get("httpMethod", None)
    http_method = event["httpMethod"]
    client_body = event["body"]
    # http_method = "POST"
    if client_body and http_method:
        if http_method == "POST":
            response_body = generateImageBySDML(client_body)
    end_time = time.time()
    execution_time = "Program Run Time : %.2f sec" % (end_time - start_time)

    return {
        "statusCode": 200,
        "body": "{}\n\n{}".format(execution_time, response_body),
        "headers": {"Content-Type": "text/plain"},
    }


def generateImageBySDML(client_prompt):
    client_bedrock = boto3.client("bedrock-runtime")
    client_s3 = boto3.client("s3")
    input_prompt = """{}""".format(client_prompt)
    response_bedrock = client_bedrock.invoke_model(
        contentType="application/json",
        accept="application/json",
        # modelId="stability.stable-diffusion-xl-v1",
        modelId="amazon.titan-text-premier-v1:0",
        body=json.dumps(
            {
                "inputText": input_prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9,
                },
            }
        ),
    )
    response_body = json.loads(response_bedrock["body"].read())
    finish_reason = response_body.get("error")
    if finish_reason is not None:
        raise Exception(f"Text generation error. Error is {finish_reason}")
    return response_body["results"][0]["outputText"]
