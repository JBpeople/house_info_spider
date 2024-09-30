import concurrent.futures
import datetime

from tqdm import tqdm

from src.config import get_config
from src.database import HouseInfo, add_house_info, query_house_info, update_house_info
from src.spider import BeiKeSpider


def parse_data(data: dict):
    """解析数据

    :param data: 数据
    """
    result = []
    for i in range(len(data["key"])):
        house_info = HouseInfo(
            key=data["key"][i],
            title=data["title"][i],
            location=data["location"][i],
            total_floor=data["total_floor"][i],
            at_floor=data["at_floor"][i],
            year=data["year"][i],
            layout=data["layout"][i],
            area=data["area"][i],
            direction=data["direction"][i],
            follower=data["follower"][i],
            upload_time=data["upload_time"][i],
            total_price=data["total_price"][i],
            unit_price=data["unit_price"][i],
        )
        result.append(house_info)
    return result


def pre_process_data():
    """数据预处理

    :param data: 数据
    """
    # 将数据库所有数据状态设置为1，表示房屋信息已经下架
    exist_house_infos = query_house_info()
    for exist_house_info in exist_house_infos:
        update_house_info(key=exist_house_info.key, status=1)


def process_data(data: dict):
    """数据处理, 将数据保存到数据库

    :param data: 数据
    """
    # 将查询到的数据状态设置为0，表示房屋信息还在出售
    house_infos = parse_data(data)
    for house_info in house_infos:
        same_house_infos = query_house_info(key=house_info.key)
        if same_house_infos:
            same_house_info = same_house_infos[0]
            update_house_info(key=same_house_info.key, status=0)
            if same_house_info.total_price != house_info.total_price:  # 判断价格是否变化
                total_price_history = eval(same_house_info.history)
                total_price_history[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = same_house_info.total_price
                update_house_info(
                    key=house_info.key,
                    total_price=house_info.total_price,
                    unit_price=house_info.unit_price,
                    history=str(total_price_history),
                )
        else:
            add_house_info(house_info)


def main():
    pre_process_data()

    url = get_config("request", "url")
    spider = BeiKeSpider(url)
    urls = spider.get_page_url()
    # 使用50个线程池提交任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(spider.get_page_data, url) for url in urls]
        # 使用tqdm展示爬取进度
        with tqdm(total=len(futures), desc="爬取进度") as pbar:
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                process_data(data)
                pbar.update(1)

    print("---> 数据爬取完成！")


if __name__ == "__main__":
    main()
