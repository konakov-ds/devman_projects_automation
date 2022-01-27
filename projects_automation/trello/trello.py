import logging
import os

import requests
from dotenv import load_dotenv

logger = logging.getLogger('logger_main')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_workspace(trello_apikey, trello_token, wrksp_name):
    url = 'https://api.trello.com/1/organizations/'
    payload = {
        'key': trello_apikey,
        'token': trello_token,
        'displayName': wrksp_name
    }
    headers = {'Accept': 'application/json'}
    
    respone = requests.post(url, data=payload, headers=headers)
    respone.raise_for_status()
    workspace = respone.json()
    logger.info(f'Create wrksp {workspace["url"]}')
    return workspace['id']

def create_board(trello_apikey, trello_token, wrksp_id, board_name, board_bg):
    url = 'https://api.trello.com/1/boards/'
    payload = {
        'key': trello_apikey,
        'token': trello_token,
        'idOrganization': wrksp_id,
        'name': board_name,
        'prefs_background': board_bg
    }
    headers = {'Accept': 'application/json'}
    
    respone = requests.post(url, data=payload, headers=headers)
    respone.raise_for_status()
    board = respone.json()
    logger.info(f'Create board {board_name}, {board["url"]}')
    return board['url']
