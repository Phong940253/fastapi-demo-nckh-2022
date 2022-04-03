from typing import Optional
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv() 
import os
TOKEN = os.environ.get("TOKEN")

app = FastAPI()

BASEURL = "https://graph.facebook.com"
VERSION = "v13.0"
data_request = {
    'access_token': TOKEN,
    'debug': 'all',
    'format': 'json',
    'method': 'get',
    'pretty': 0,
    'suppress_http_code': 1,
    'transport': 'cors',
    'fields': 'feed{comments{comments,message},message}'
}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/get-post-group/{page_id}")
async def get_post_group(page_id):
    r = requests.get(BASEURL + "/" + VERSION + "/" + page_id, params=data_request)
    print(r.url)
    return r.json()