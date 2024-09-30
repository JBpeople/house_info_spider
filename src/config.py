import configparser

_CONFIG_PATH = "static/config.ini"


def get_config(section: str, key: str):
    """获取配置

    :param section: 配置段
    :param key: 配置键
    :return: 配置值
    """
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        try:
            return config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None


def add_config(section: str, key: str, value: str):
    """添加配置

    :param section: 配置段
    :param key: 配置键
    :param value: 配置值
    """
    config = configparser.ConfigParser()
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        config.read_file(f)
    if not config.has_section(section):  # 如果配置段不存在，则添加
        config.add_section(section)
    config.set(section, key, value)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def delete_config(section: str, key: str):
    """删除配置

    :param section: 配置段
    :param key: 配置键
    """
    config = configparser.ConfigParser()
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        config.read_file(f)
        config.remove_option(section, key)
        options = config.items(section)
        if not options:
            config.remove_section(section)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def update_config(section: str, key: str, value: str):
    """更新配置

    :param section: 配置段
    :param key: 配置键
    :param value: 配置值
    """
    config = configparser.ConfigParser()
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        config.read_file(f)
        config.set(section, key, value)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)
