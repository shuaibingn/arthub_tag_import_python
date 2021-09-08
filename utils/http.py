import logging

import requests


def post(url, data=None, json=None, **kwargs) -> dict:
    try:
        resp = requests.post(url, data, json, **kwargs)
        resp_data = resp.json()
    except Exception as e:
        logging.error(f"request {url} error, {e}")
        return {}

    return resp_data


def get(url, params=None, **kwargs) -> dict:
    try:
        resp = requests.get(url, params, **kwargs)
        resp_data = resp.json()
    except Exception as e:
        logging.error(f"request {url} error, {e}")
        return {}

    return resp_data
