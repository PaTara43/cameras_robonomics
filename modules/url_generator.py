import ast
import logging
import requests

from typing import Tuple, Any


def create_url(config: dict) -> Tuple[Any, Any]:

    try:
        url = "https://" + config["yourls"]["server"] + "/yourls-api.php"
        querystring = {
            "username": config["yourls"]["username"],
            "password": config["yourls"]["password"],
            "action": "shorturl",
            "format": "json",
            "url": "http://gateway.ipfs.io",
        }
        payload = ""
        response = requests.request("GET", url, data=payload, params=querystring)

        logging.debug(response.text)
        keyword = ast.literal_eval(response._content.decode("utf-8"))["url"]["keyword"]
        link = config["yourls"]["server"] + "/" + keyword
        return keyword, link
    except Exception as e:
        logging.warning("Failed to create URL, replaced by url.today/55. Error: ", e)
        return "55", "url.today/55"


def update_url(keyword: str, hash: str, config: dict) -> None:

    try:
        url = "https://" + config["yourls"]["server"] + "/yourls-api.php"
        querystring = {
            "username": config["yourls"]["username"],
            "password": config["yourls"]["password"],
            "action": "update",
            "format": "json",
            "url": "http://gateway.ipfs.io/ipfs/" + hash,
            "shorturl": keyword,
        }
        payload = ""
        response = requests.request("GET", url, data=payload, params=querystring)

        logging.debug(response)
    except Exception as e:
        logging.warning("Failed to update URL: ", e)
