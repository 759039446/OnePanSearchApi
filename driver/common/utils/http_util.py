import asyncio
from urllib.parse import urljoin

import aiohttp
import requests


def send_post_request(url, body, headers=None, timeout=10, params=None):
    """
    发送一个 POST 请求到指定的 URL，请求体为字典。

    参数:
    url (str): 请求的 URL。
    body (dict): 请求体，字典格式。
    headers (dict, optional): 请求头，默认为 None。
    timeout (int, optional): 请求超时时间，默认为 10 秒。

    返回:
    response (requests.Response): 请求的响应对象。
    """
    try:
        # 如果没有提供 headers，则设置一个默认的 headers
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        # 发送 POST 请求
        if isinstance(body, dict):
            response = requests.post(url, json=body, headers=headers, timeout=timeout, params=params)
        else:
            response = requests.post(url, data=body, headers=headers, timeout=timeout, params=params)
        # 返回响应对象
        if response:
            return response.json()

    except Exception as e:
        # 捕获并打印请求异常
        print(f"请求异常|| {e}")
    return None


def send_get_request(url, params=None, headers=None):
    """
    发送一个GET请求到指定的URL。

    参数:
    url (str): 请求的URL。
    params (dict, optional): 查询参数。默认为None。
    headers (dict, optional): 请求头。默认为None。

    返回:
    response (requests.Response): 请求的响应对象。
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        return response.json()
    except Exception as e:
        return None


def send_get_request_text(url, params=None, headers=None):
    """
    发送一个GET请求到指定的URL。

    参数:
    url (str): 请求的URL。
    params (dict, optional): 查询参数。默认为None。
    headers (dict, optional): 请求头。默认为None。

    返回:
    response (requests.Response): 请求的响应对象。
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        return response.text
    except Exception as e:
        return None


async def aio_request(method: str, url: str, **kwargs) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            return await response.text()


def send_request(method: str, url: str, **kwargs) -> str:
    aio_data = []

    async def func():
        aio_data.append(await aio_request(method, url, **kwargs))

    looper = asyncio.new_event_loop()
    looper.run_until_complete(func())
    return aio_data[0]
