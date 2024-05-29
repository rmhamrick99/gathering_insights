import asyncio
import os, types
import getpass
import numpy as np
import pandas as pd
from ibm_watson_machine_learning.foundation_models import Model
from dotenv import load_dotenv
import requests
import json
load_dotenv()

index = 0
apikey = os.getenv("GENAI_API")
project_id = os.getenv("GENAI_PRO_ID")
url = "https://us-south.ml.cloud.ibm.com"
creds= {
		"url" : url,
        "apikey": apikey
	}

def getToken():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': apikey,
    }
    response = requests.post('https://iam.cloud.ibm.com/identity/token', headers=headers, data=data, verify=False)
    json_reponse = json.loads(response.content)
    token = json_reponse['access_token']
    return token

def custom_model(data, prompt_template, model_params):
    token = getToken()
    prompt_data = prompt_template + "\n\n Input: " + data + "\n Output: "
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
        }
    params = {
        'version': '2023-05-29',
    }
    json_data = {
        'input': prompt_data,
        'parameters': model_params,
        # 'parameters': {
        #     'decoding_method': 'greedy',
        #     'max_new_tokens': 100,
        #     'min_new_tokens': 0,
        #     'stop_sequences': [],
        #     'repetition_penalty': 1,
        # },
    }

    response = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v1-beta/deployments/ee7d6ab7-f49f-4a33-b948-5fa312979799/generation/text',
        params=params,
        headers=headers,
        json=json_data,
    )
    result = json.loads(response.content)
    return(result['results'][0]['generated_text'])


