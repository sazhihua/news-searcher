import os
import random
import traceback
import uuid

import jieba
from wordcloud import WordCloud

from searchApp.config import logger
from searchApp.core.utils import funcUtils

log = logger.createLogger("cloudPicUtils")


def buildCloudPic(infos):
    """
    生成云图函数
    :return:
    """
    try:
        log.info('正在为选择的页面生成云图图像...')
        stopwords = stopwordsList(os.getcwd() + '\\searchApp\\help\\stop_words.txt')

        word_count = {}
        for info in infos:
            key_words = jieba.lcut(info['title'], cut_all=False)
            for word in key_words:
                # if word != '' and word not in stopwords and not funcUtils.objIsNumber(word) and not word.isspace():
                if len(word) >= 2 and word not in stopwords and not funcUtils.objIsNumber(word) and not word.isspace():
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

        # 生成云图
        wc = WordCloud(
            background_color="white",  # 背景颜色
            max_words=200,  # 显示最大词数
            font_path=os.getcwd() + '\\static\\font\\msyh.ttc',  # 使用字体
            min_font_size=15,
            max_font_size=50,
            width=500,
        ).generate_from_frequencies(word_count)

        fileName = str(uuid.uuid4())
        filePath = os.getcwd() + '\\static\\img\\cloudpic\\' + fileName + '.png'
        wc.to_file(filePath)
        log.info('生成成功，文件名：{}'.format(fileName))

        word_key = list(word_count.keys())
        for item in word_key[:]:
            if len(item) < 2:
                word_key.remove(item)

        return {'id': fileName,
                'list': random.sample(word_key, 10) if len(word_key) > 10 else random.sample(word_key, len(word_key))}

    except Exception as e:
        traceback.print_exc()
        log.error('生成云图失败，错误信息：{}'.format(e))
        return False


# 创建停用词list
def stopwordsList(filepath):
    with open(filepath, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    stopwords = [c.strip() for c in lines]
    return stopwords


def deleteAllCloudPics():
    """
    用于定时删除云图文件夹中的图像
    :return:
    """
    path = os.getcwd() + '\\static\\img\\cloudpic'
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        os.remove(c_path)
