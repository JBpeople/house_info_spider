import requests

from src.config import get_config

_BODY = {
    "appToken": "",
    "content": "",
    "summary": "",
    "contentType": 3,
    "topicIds": [],
    "verifyPayType": 0,
}


def push_message(summary: str, content: str):
    """推送消息到wxpusher

    :param summary: 消息摘要
    :param content: 消息内容
    """
    # 如果wxpusher未启用，则不推送
    if get_config("wxpusher", "enable").upper() != "TRUE":
        return
    # 设置appToken
    _BODY["appToken"] = get_config("wxpusher", "app_token")
    # 设置topicId
    _BODY["topicIds"] = [int(get_config("wxpusher", "topic_id"))]
    # 设置摘要
    _BODY["summary"] = summary
    # 设置内容
    _BODY["content"] = content
    # 设置请求头
    headers = {"Content-Type": "application/json"}
    requests.post("https://wxpusher.zjiecode.com/api/send/message", json=_BODY, headers=headers)
