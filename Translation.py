# _*_ coding:utf-8

import requests
from HandleJs import Py4Js
from config import url, test_content
from config import logger, get_header


def translate(tk, content):
    if len(content) > 4891:
        logger.error("翻译的长度超过限制！！！")
        return

    param = {'tk': tk, 'q': content}

    result = requests.get(url, params=param, headers=get_header()).json()

    # 返回的结果为Json，解析为一个嵌套列表
    return result


def main():
    js = Py4Js()
    content = test_content
    tk = js.getTk(content)
    res = translate(tk, content)
    print(res)


if __name__ == "__main__":
    main()