# _*_ coding:utf-8 _*_

"""
存储一些翻译基本配置以及logger输出
"""
import logging
import os


# Google翻译 API
url = """http://translate.google.cn/translate_a/single?client=t&sl=en
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2"""

# 批量翻译时多进程数目设置
pool_num = 8

# 测试case
test_content = """Beautiful is better than ugly.Explicit is better than implicit.Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        Special cases aren't special enough to break the rules.
        Although practicality beats purity.
        Errors should never pass silently.
        Unless explicitly silenced.
        In the face of ambiguity, refuse the temptation to guess.
        There should be one-- and preferably only one --obvious way to do it.
        Although that way may not be obvious at first unless you're Dutch.
        Now is better than never.
        Although never is often better than *right* now.
        If the implementation is hard to explain, it's a bad idea.
        If the implementation is easy to explain, it may be a good idea.
        Namespaces are one honking great idea -- let's do more of those!"""

# 定制logger
def get_logger():
    logger_obj = logging.getLogger()

    fh = logging.FileHandler('translation.log', encoding='utf-8')
    fh.setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formater = logging.Formatter('%(pathname)s - %(lineno)s - %(levelname)s - %(message)s')
    fh.setFormatter(formater)
    ch.setFormatter(formater)

    logger_obj.addHandler(fh)
    logger_obj.addHandler(ch)

    return logger_obj

logger = get_logger()