from abc import ABC, abstractmethod

import requests

from src.err import HumanMachineVerificationError
from src.spider.cookie import get_beike_cookie
from src.spider.human_verification import BeiKeHumanVerification


class WebPage(ABC):
    """网页抽象类"""

    @abstractmethod
    def get_html(self) -> str:
        """获取网页内容

        :return: 网页内容
        """
        pass


class BeikeWebPage(WebPage):
    """贝壳网页"""

    def __init__(self, url: str):
        self.url = url

    def check_html(self, html: str) -> bool:
        """检查网页内容是否需要人机验证

        :param html: 网页内容
        :return: 是否需要人机验证
        """
        if "你的访问已触发人机验证，请按指示操作" in html:
            return True
        elif '<div id="loginHolder"></div>' in html:
            return True
        else:
            return False

    def get_html(self) -> str:
        """获取网页内容

        :return: 网页内容
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Connection": "keep-alive",
        }
        cookie = get_beike_cookie()
        response = requests.get(self.url, headers=headers, cookies=cookie)
        if self.check_html(response.text):
            BeiKeHumanVerification().do_human_verify()
            cookie = get_beike_cookie()
            response = requests.get(self.url, headers=headers, cookies=cookie)
            if self.check_html(response.text):
                raise HumanMachineVerificationError("人机验证失败")
            else:
                return response.text
        else:
            return response.text


class LocoalWebPage(WebPage):
    """本地网页测试案例使用"""

    def __init__(self, html_path: str):
        self.html_path = html_path

    def get_html(self) -> str:
        """获取本地网页内容

        :return: 网页内容
        """
        with open(self.html_path, "r", encoding="utf-8") as f:
            return f.read()
