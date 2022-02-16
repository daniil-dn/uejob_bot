import re
import os.path
import requests
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlparse


class StopGame:
    host = "https://stopgame.ru"
    url = "https://stopgame.ru/review/new"

    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file
