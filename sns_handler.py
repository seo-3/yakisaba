import boto3
import json
import requests
from urllib.error import URLError, HTTPError
import time
from os import getenv

epoch = int(time.time())
API_KEY = getenv("MACKEREL_API_KEY")
SERVICE_NAME = getenv("SERVICE")


def postServiceMetric(api_key, service, payload):

    url = "https://mackerel.io/api/v0/services/" + service + "/tsdb"
    headers = {'Content-Type': 'application/json', 'X-Api-Key' : api_key}

    return requests.post(url, data=json.dumps(payload), headers=headers)

def lambda_handler(event, context):

    print("Received event: " + str(event))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    print("Message: " + str(message))

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']

    payload = [{"name" : "sns." + alarm_name + "." + new_state, "time" : epoch, "value" : 1}]

    print(json.dumps(payload))

    try:
        res = postServiceMetric(api_key=API_KEY,
            service=SERVICE_NAME,
            payload=payload)

        print("Message posted to ", res.json)

    except HTTPError as e:
        print("Request failed: ", e.reason)
    except URLError as e:
        print("Server connection failed: ", e.reason)

if __name__ == "__main__":

	f = open("event.json", "r")

	event = json.load(f)
	context = ""
	f.close()

	lambda_handler(event, context)
