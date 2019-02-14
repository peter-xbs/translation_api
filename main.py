# _*_ coding:utf-8 _*_

import requests
import time
import random
from Translation import translate
from HandleJs import Py4Js
from multiprocessing.dummy import Pool as ThreadPool
from config import logger, pool_num


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def extract_info_from_translation(translation):
    """暴力方式，效率低"""
    translation_new = []
    translation_last = []
    for item in translation:
        if item == '':
            continue
        elif item is None:
            continue
        elif not check_contain_chinese(str(item)):
            continue
        for elem in item:
            if not check_contain_chinese(str(elem)):
                continue
            for term in elem:
                if not check_contain_chinese(str(term)):
                    continue
                if isinstance(term, str):
                    translation_new.append(term)
                else:
                    term = [x for x in term if isinstance(x, list)]
                    for x in term:
                        for y in x:
                            if check_contain_chinese(str(y)):
                                translation_new.append(y)
    for para in translation_new:
        if para not in translation_last:
            translation_last.append(para)
    translation_result = ''.join(translation_last)
    return translation_result


def extract_translation(translation):
    """仔细研究翻译返回结果抽象出来的高效率方式"""
    output_list = []
    best_res = translation[0]  # 第一部分应该是最佳翻译结果
    for sent_tup in best_res[:-1]:
        sent = sent_tup[0]
        if not isinstance(sent, str):
            logger.error("服务返回翻译结果格式无法解析，请检查解析程序....")
            return
        if not check_contain_chinese(sent):  # 返回结果中不包含中文字符，可能翻译效果不是很好
            logger.error("服务返回翻译结果中不包含中文字符，请检查返回翻译结果内容是否符合要求....")
        output_list.append(sent)
    return '\n'.join(output_list)


def combine_translate(tp):
    global fo
    tp = list(tp)
    term_en = tp[1]
    tk = Py4Js().getTk(term_en)
    t = random.choice([0.5, 0.45, 0.35, 0.25, 0.15, 0.05])
    time.sleep(t)
    try:
        translation = translate(tk, term_en)
        if not isinstance(translation, list) or len(translation) < 9:
            logger.error("请求翻译服务失败，返回了错误的结果，请检查....")
            result = 'NULL'
        else:
            result = extract_translation(translation)
        tp.append(result)
        new_line = '\t'.join(tp)+'\n'
        return new_line
    except Exception as e:
        return


def parallel_translate(input, output, pool_num):
    """
    批量翻译，接受文件格式见example_input，可以为1列内容；若为多列信息，请将待翻译内容放置最后一列，并与
    其余列用\t隔开
    """
    with open(input, 'r', encoding='utf-8') as f, open(output, 'w', encoding='utf-8') as fo:
        pool = ThreadPool(pool_num)
        input_list = []
        for line in f:
            line = line.strip()
            line_list = line.split('\t')
            prefix_info = '\t'.join(line_list[:-1])
            translation_en = line_list[-1]
            # todo 自定义条件，根据需求调整
            if not translation_en == '[not available]':
                tup = (prefix_info, translation_en)
                input_list.append(tup)
        for res in pool.imap_unordered(combine_translate, input_list, chunksize=1000):
            # imap is much slower than map, if you don't concern the order, using imap_unordered, which much
            # faster than the imap
            fo.write(str(res))
        pool.close()
        pool.join()


if __name__ == '__main__':
    inp = 'example_input'
    output = 'temp'
    parallel_translate(inp, output, pool_num)

