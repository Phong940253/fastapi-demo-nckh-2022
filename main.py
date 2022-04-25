import os
from typing import Optional, Dict
import requests
from fastapi import FastAPI
from dotenv import load_dotenv

from support import get_model, padding_data, get_label
from typing import List
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
def get_list_groups():
    url = BASEURL + "/" + VERSION + "/me"
    payload['fields'] = "groups{administrator,name}"
    response = requests.get(url, params=payload).json()
    # print(response)
    if 'groups' in response and 'data' in response['groups']:
        res = response['groups']['data']
        response = response['groups']
        while 'paging' in response and 'next' in response['paging']:
            response = requests.get(response['paging']['next']).json()
            res = res + response['data']
    else:
        res = []
    return res


@app.get("/groups/admin")
def get_list_groups_admin():
    list_group = get_list_groups()
    list_group = [group for group in list_group if group['administrator']]
    return list_group


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
def get_list_post_group(group_id: str):
    payload['fields'] = 'feed{comments{message,from,created_time,comments{message,from,created_time}},message,from,created_time}'
    response = requests.get(
        BASEURL +
        '/' +
        VERSION +
        '/' +
        group_id,
        params=payload).json()

    res = response['feed']['data']
    response = response['feed']
    while 'paging' in response and 'next' in response['paging']:
        response = requests.get(response['paging']['next']).json()
        res = res + response['data']
    for post in res:
        if "message" in post:
            poster = post["message"]
            if "comments" in post:
                for comment in post["comments"]["data"]:
                    if "message" in comment:
                        comment_label = get_label(
                            poster, comment["message"], model)
                        print(comment_label)
                        comment["label"] = round(comment_label[0][0])
                    if "comments" in comment:
                        for sub_comment in comment["comments"]["data"]:
                            if "message" in sub_comment:
                                comment_label = get_label(
                                    poster, sub_comment["message"], model)
                                print(comment_label)
                                sub_comment["label"] = round(
                                    comment_label[0][0])
    print(res)
    return res


# @app.post("/analysis")
# def get_analysis(array_post: List[str], array_comment: List[str]):

#     print(len(array_post))
#     print(len(array_comment))
#     return model.predict({"Poster": array_post, "Comments": array_comment})


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

model = get_model()
model.load_weights("model/model.hdf5")
