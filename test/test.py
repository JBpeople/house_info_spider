from src.database.db import query_house_info

house_infos = query_house_info(key=1)
for house_info in house_infos:
    print(house_info.key)
