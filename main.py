# _*_ coding:utf-8 _*_

import requests
import time
import random
from Translation import translate
from HandleJs import Py4Js
from multiprocessing.dummy import Pool as ThreadPool
import re

pool = ThreadPool(8)


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def extract_info_from_translation(translation):
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


def combine_translate(tp):
    global fo
    tp = list(tp)
    term_en = tp[1]
    tk = Py4Js().getTk(term_en)
    t = random.choice([0.5, 0.75, 1, 1.25, 1.5])
    time.sleep(t)
    try:
        translation = translate(tk, term_en)
        try:
            result = extract_info_from_translation(translation)
        except Exception as e:
            result = 'NULL'
        tp.append(result)
        new_line = '\t'.join(tp)+'\n'
        return new_line
    except Exception as e:
        return


def parallel_translate(input, output, pool_num):
    """
    批量翻译
    """
    with open(input, 'r', encoding='utf-8') as f, open(output, 'w', encoding='utf-8') as fo:
        pool = ThreadPool(pool_num)
        input_list = []
        for line in f:
            line = line.strip()
            line_list = line.split('\t')
            prefix_info = line_list[0]+'\t'+line_list[1]
            translation_en = line_list[2]
            if not translation_en == '[not available]':
                tup = (prefix_info, translation_en)
                input_list.append(tup)
        for res in pool.imap(combine_translate, input_list, chunksize=100):
            # imap is much slower than map, if you don't concern the order, using imap_unordered, which much
            # faster than the imap
            fo.write(str(res))
        pool.close()
        pool.join()


if __name__ == '__main__':
    inp = 'test'
    output = 'temp'
    parallel_translate(inp, output, 1)

