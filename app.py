import uvicorn
from fastapi import FastAPI, Request
import logging
import json
import requests

logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger(__name__)

app = FastAPI()


# Query string based
@app.get('/get_resources')
async def get_data(request: Request):
    api_key = request.headers.get('api_key')
    data = create_resource_group(api_key)
    json_data = json.loads(data)
    return json_data["resources"]

def get_iam_token(api_key):
    iam_url = 'https://iam.cloud.ibm.com/identity/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'apikey': api_key,
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
    }
    response = requests.post(iam_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to generate IAM token. Status code: {response.status_code}, Error message: {response.text}")
        return None

def create_resource_group(api_key):
    iam_token = get_iam_token(api_key)
    if not iam_token:
        return
    resource_controller_url = 'https://resource-controller.cloud.ibm.com/v2/resource_instances'
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(resource_controller_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return (f"Failed to create resource group. Status code: {response.status_code}, Error message: {response.text}")


if __name__ == "__main__": 
    uvicorn.run(app, host='127.0.0.1', port=8080)
