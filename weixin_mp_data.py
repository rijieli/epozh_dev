import requests
import re

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
    resp = requests.get(url)
    if(resp.status_code == 200):
        return resp.text;
    else:
        raise ConnectionError()


url = "https://mp.weixin.qq.com/s/-y8d-65hRDNPXB13EWlMTA"

# url = "https://epozh.cn/"

# requestHTML(url)

def read_chunk(target_file, chunk_size=1024):
    while True:
        line = target_file.readline()
        if not line:
            break
        yield line

def parseData(content):

    # 定义关键正则表达式
    # 标题
    TITLE_REGEX = r'''var msg_title = \'([\u4e00-\u9fa5_a-zA-Z0-9\s\S]+)\'\.html'''
    # 日期
    DATE_REGEX = r'''s=\"(2020-\w+-\w+)\"'''
    # URL
    # 作者
    AUTHOR_REGEX = r'''\<meta name=\"author\" content\=\"([\u4e00-\u9fa5_a-zA-Z0-9]+)\" \/\>'''
    # 封面图
    HEADER_IMAGE_REGEX = r'''var msg_cdn_url = \"([\w\:\/\.\?\_\=]+)\"\;'''

    m = re.match(TITLE_REGEX, content)
    print(m.group)

with open("./wesample.html", "r") as target:
    content = target.read()
    parseData(content)