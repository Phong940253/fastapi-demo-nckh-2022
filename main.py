import os
from typing import Optional
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("TOKEN")

app = FastAPI()

BASEURL = "https://graph.facebook.com"
VERSION = "v13.0"
payload = {
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


@app.get("/pages")
async def get_list_pages():
    url = BASEURL + "/" + VERSION + "/me/feed"
    response = requests.get(url, params=payload)
    return response.json()


@app.get("/groups")
async def get_list_groups():
    url = BASEURL + "/" + VERSION + "/me"
    payload['fields'] = "groups{permissions,name}"
    response = requests.get(url, params=payload).json()
    # print(response)
    res = response['groups']['data']
    response = response['groups']
    while 'paging' in response and 'next' in response['paging']:
        response = requests.get(response['paging']['next']).json()
        res = res + response['data']
    return res


@app.get("/groups/admin")
async def get_list_groups_admin():
    pass


@app.get("/page/{page_id}")
async def get_list_post_page(page_id: str):
    response = requests.get(
        BASEURL +
        '/' +
        VERSION +
        '/' +
        page_id,
        params=payload)
    return response.json()


@app.get("/group/{group_id}")
async def get_list_post_group(group_id: str):
    response = requests.get(
        BASEURL +
        '/' +
        VERSION +
        '/' +
        group_id,
        params=payload)
    return response.json()


@app.get("/post/{post}")
async def get_post_group(post: str):
    payload['fields'] = 'feed{comments{comments,message},message}'
    response = requests.get(
        BASEURL +
        "/" +
        VERSION +
        "/" +
        post,
        params=payload)
    return response.json()
