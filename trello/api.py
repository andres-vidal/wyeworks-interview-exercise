from requests import get, post, put, delete
from utils import request

from threading import Thread

import json


# Constants

TRELLO_API = "https://api.trello.com/1"


# Load credentials

with open('trello/credentials.json', 'r') as f:
    credentials = json.load(f)

TRELLO_CLIENT_ID = credentials["TRELLO_CLIENT_ID"]
TRELLO_ACCESS_TOKEN = credentials["TRELLO_ACCESS_TOKEN"]


# API Calls


def create_board(name):

    target = f"{TRELLO_API}/boards"

    params = {
        "name": name,
        "defaultLists": "false",
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    return request(post, target, params).json()["id"]


def create_list(name, board_id):

    target = f"{TRELLO_API}/lists"

    params = {
        "name": name,
        "idBoard": board_id,
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    return request(post, target, params).json()["id"]


def create_card(name, list_id):

    target = f"{TRELLO_API}/cards"

    params = {
        "name": name,
        "idList": list_id,
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    return request(post, target, params).json()["id"]


def create_attachment(url, card_id):

    target = f"{TRELLO_API}/cards/{card_id}/attachments"

    params = {
        "url": url,
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    return request(post, target, params).json()["id"]


def set_card_cover(card_id, attachment_id):

    target = f"{TRELLO_API}/cards/{card_id}"

    params = {
        "idAttachmentCover": attachment_id,
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    request(put, target, params)


def close_and_delete_board(board_id):

    target = f"{TRELLO_API}/boards/{board_id}"

    params = {
        "closed": "true",
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    request(put, target, params)
    request(delete, target, params)


def delete_boards(name):

    target = f"{TRELLO_API}/search"

    params = {
        "query": name,
        "modelTypes": "boards",
        "boards_limit": "1000",
        "key": TRELLO_CLIENT_ID,
        "token": TRELLO_ACCESS_TOKEN
    }

    boards = request(get, target, params).json()["boards"]
    board_ids = [board["id"] for board in boards]

    threads = []

    for board_id in board_ids:
        t = Thread(target=close_and_delete_board, args=(board_id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
