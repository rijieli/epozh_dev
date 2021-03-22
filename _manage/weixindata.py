from os import nice
from typing import OrderedDict
import requests
import re
import csv

# 定义关键正则表达式
TITLE_REGEX = re.compile(
    r'''var msg_title = \'([\u4e00-\u9fa5_a-zA-Z0-9\s\S]+)\'\.html\(false\);''')
DATE_REGEX = re.compile(r'''s=\"(\d+-\w+-\w+)\"''')
AUTHOR_REGEX = re.compile(
    r'''\<meta name=\"author\" content\=\"([\u4e00-\u9fa5_a-zA-Z0-9]+)\" \/\>''')
HEADER_IMAGE_REGEX = re.compile(
    r'''var msg_cdn_url = \"([\w\:\/\.\?\_\=]+)\"\;''')
NICKNAME_REGEX = re.compile(r'''nickname = \"([\u4e00-\u9fa5_a-zA-Z0-9]+)\"''')

headers = {
    'Host': 'mp.weixin.qq.com',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'zh-cn',
    'origin': 'https://mp.weixin.qq.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/2.5(0x12050010) Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat',
}


def requestHTML(url):
    '''
    获取页面 HTML 文档
    '''

    resp = requests.get(url)
    if(resp.status_code == 200):
        return resp.text
    else:
        raise ConnectionError()


def parseData(content, match_group):
    '''
    正则表达式逐个匹配关键信息
    '''
    result = {}
    for item in match_group:
        m = item[1].findall(content)
        if(len(m) > 0):
            result[item[0]] = m[0]

    return result


def match_meta_info(content):
    '''
    解析 HTML 文档中的关键信息
    '''

    # 此处存在硬编码，需要注意与 CSV 文件对应
    MATCH_GROUP = [("title", TITLE_REGEX), ("date", DATE_REGEX),
                   ("author", AUTHOR_REGEX), ("alt_img_url", HEADER_IMAGE_REGEX), ("nickname", NICKNAME_REGEX)]

    result = parseData(content, MATCH_GROUP)

    if not result.get("author"):
        result["author"] = result["nickname"]

    result.pop("nickname")

    if len(result) != (len(MATCH_GROUP) - 1):
        raise RuntimeError()

    return result


def get_image(img_url, row):
    '''
    下载封面图
    '''
    if not img_url.startswith("http"):
        img_url += "http://"

    target_path = "./assets/img/archives/posts/" + \
        "{id}.jpeg".format(id=row["url"][-6:])

    r = requests.get(img_url)
    local_file = open(target_path, "wb")
    for chunk in r.iter_content(10000):
        local_file.write(chunk)

    local_file.close()


def get_info(row: OrderedDict):

    result = ",".join(row.values())

    try:
        content = requestHTML(row["url"])
        matched_meta_info = match_meta_info(content)
        get_image(matched_meta_info["alt_img_url"], row)
    except Exception as i:
        print(i)
        print("Parsed Faild: " + row["url"])
        return result

    row.update(matched_meta_info)

    # Add local image path
    row["img_path"] = "/assets/img/archives/posts/" + \
        "{id}.jpeg".format(id=row["url"][-6:])

    print("解析成功：#" + row["id"] + " " + row["title"])
    return ",".join(row.values())


def fill_default(row):
    if not row["platform"] and ("weixin" in row["url"]):
        row["platform"] = "weixin"

    if not row["data_type"] and ("weixin" in row["url"]):
        row["data_type"] = "visit"


def write_csv():
    csv_updated = ""

    row_idx = 0

    with open("./_data/archives.csv", 'r') as csv_file:
        creader = csv.DictReader(csv_file)
        csv_updated = csv_updated + ",".join(creader.fieldnames) + "\n"
        for row in creader:
            if row["id"]:
                row_idx = int(row["id"])
            else:
                row_idx += 1
                row["id"] = str(row_idx)
            
            fill_default(row)

            if not row["title"] and row["url"]:
                filed_row = get_info(row)
                csv_updated = csv_updated + filed_row + "\n"
            else:
                csv_updated = csv_updated + ",".join(row.values()) + "\n"

    csv_updated = csv_updated[:-1]

    with open("./_data/archives.csv", 'w') as csv_file:
        csv_file.write(csv_updated)


write_csv()
