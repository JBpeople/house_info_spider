import re
from abc import ABC, abstractmethod

from lxml import etree


class PageContentHandler(ABC):
    """网页内容处理器抽象类

    :param ABC: 抽象类
    """

    @abstractmethod
    def _parse_html(self) -> dict:
        """解析网页内容

        :return: 解析后的网页内容
        """
        pass

    @abstractmethod
    def parse_data(self) -> dict:
        """解析数据

        :return: 解析后的数据
        """
        pass


class BeiKePageHandler(PageContentHandler):
    """贝壳网页"""

    def __init__(self, html: str):
        self.html = html

    def _parse_html(self) -> dict:
        """解析网页内容

        :return: 解析后的网页内容
        """
        html_tree = etree.HTML(self.html)
        # 获取数据
        key = html_tree.xpath('//li[@class="clear"]/a/@href')
        title = html_tree.xpath('//li[@class="clear"]/a/@title')
        location = html_tree.xpath('//div[@class="positionInfo"]/a/text()')
        house_info = html_tree.xpath('//div[@class="houseInfo"]/text()')
        house_info = [i for i in house_info if i.strip()]
        follow_info = html_tree.xpath('//div[@class="followInfo"]/text()')
        follow_info = [i for i in follow_info if i.strip()]
        total_price = html_tree.xpath('//div[@class="totalPrice totalPrice2"]/span/text()')
        unit_price = html_tree.xpath('//div[@class="unitPrice"]/span/text()')
        result = {
            "key": key,
            "title": title,
            "location": location,
            "house_info": house_info,
            "follow_info": follow_info,
            "total_price": total_price,
            "unit_price": unit_price,
        }
        return result

    def _parse_house_info(self, house_infos: list[str]) -> list[dict]:
        """解析房屋信息

        :param house_info: 房屋信息
        :return: 解析后的房屋信息
        """
        # 编写正则表达式
        total_floor_pattern = re.compile(r"(\d+)层")
        at_floor_pattern = re.compile(r"(低楼层|中楼层|高楼层)")
        year_pattern = re.compile(r"(\d+)年")
        layout_pattern = re.compile(r"(\d+室\d+厅)")
        area_pattern = re.compile(r"(\d+(\.\d+)?)平米")
        direction_pattern = re.compile(r"(东|南|西|北)")

        result = []
        # 遍历房屋信息
        for house_info in house_infos:
            # 解析房屋信息
            total_floor = total_floor_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            at_floor = at_floor_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            year = year_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            layout = layout_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            area = area_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            direction = direction_pattern.search(house_info).group(1)  # type: ignore[union-attr]
            result.append(
                {
                    "total_floor": int(total_floor),
                    "at_floor": at_floor,
                    "year": int(year),
                    "layout": layout,
                    "area": float(area),
                    "direction": direction,
                }
            )
        return result

    def _parse_follow_info(self, follow_info: list[str]) -> list[dict]:
        """解析关注信息

        :param follow_info: 关注信息
        :return: 解析后的关注信息
        """
        follower_pattern = re.compile(r"(\d+)人")
        upload_time_pattern = re.compile(r"(今天|\d+天|\d+月|\d+年)")

        result = []
        # 遍历关注信息
        for info in follow_info:
            follower = follower_pattern.search(info).group(1)  # type: ignore[union-attr]
            upload_time_str = upload_time_pattern.search(info).group(1)  # type: ignore[union-attr]
            if upload_time_str == "今天":
                upload_time = 0
            else:
                upload_time = int(upload_time_str[:-1])
            upload_time_unit = upload_time_str[-1]
            # 根据单位转换时间
            match upload_time_unit:
                case "天":
                    upload_time = upload_time
                case "月":
                    upload_time = upload_time * 30
                case "年":
                    upload_time = upload_time * 365
            result.append(
                {
                    "follower": int(follower),
                    "upload_time": upload_time,
                }
            )
        return result

    def parse_data(self) -> dict:
        """解析数据

        :return: 解析后的数据
        """
        data = self._parse_html()
        result = {}
        for key, value in data.items():
            if key == "key":
                value = [i.split("/")[-1] for i in value]
                value = [int(i.split(".")[0]) for i in value]
                result[key] = value
            elif key == "house_info":
                ser_house_info = self._parse_house_info(value)
                result["total_floor"] = [i["total_floor"] for i in ser_house_info]
                result["at_floor"] = [i["at_floor"] for i in ser_house_info]
                result["year"] = [i["year"] for i in ser_house_info]
                result["layout"] = [i["layout"] for i in ser_house_info]
                result["area"] = [i["area"] for i in ser_house_info]
                result["direction"] = [i["direction"] for i in ser_house_info]
            elif key == "follow_info":
                ser_follow_info = self._parse_follow_info(value)
                result["follower"] = [i["follower"] for i in ser_follow_info]
                result["upload_time"] = [i["upload_time"] for i in ser_follow_info]
            elif key == "total_price":
                result[key] = [float(i) for i in value]
            elif key == "unit_price":
                result[key] = [float(re.sub(r"\D", "", i)) for i in value]
            else:
                result[key] = value
        return result


class PageNumHandler(ABC):
    """网页页数处理器抽象类

    :param ABC: 抽象类
    """

    @abstractmethod
    def get_page_num(self) -> int:
        pass


class BeiKePageNumHandler(PageNumHandler):
    """贝壳网页页数处理器"""

    def __init__(self, html: str):
        self.html = html

    def get_page_num(self) -> int:
        """获取网页页数

        :return: 网页页数
        """
        html_tree = etree.HTML(self.html)
        page_num = html_tree.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')
        ser_page_num = eval(page_num[0])
        return ser_page_num["totalPage"]
