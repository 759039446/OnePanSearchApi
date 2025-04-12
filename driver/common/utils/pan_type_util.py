from urllib.parse import urlparse

# 网盘类型映射配置（可修改），如果没有，则为其他
DISK_TYPE_MAPPING = {
    "pan.baidu.com": "百度网盘",
    "pan.quark.cn": "夸克网盘",
    "pan.xunlei.com": "迅雷网盘",
    "www.alipan.com": "阿里网盘",
    'drive.uc.cn': 'UC网盘'
}


def get_pan_type(url: str) -> str:
    """
    获取网盘类型
    :param url: 网盘链接
    :return: 网盘类型
    """
    domain = urlparse(url).netloc
    return DISK_TYPE_MAPPING.get(domain, "其他")
