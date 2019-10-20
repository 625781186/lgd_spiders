# -*- coding: utf-8 -*-
# @Time    : 2019/10/13 9:13
# @Author  : LGD
# @File    : ciyun.py
# @功能    : 根据商品评论制作词云


# 引入模块
import csv
import numpy as np
import PIL.Image as image
import jieba
from wordcloud import WordCloud


# 获取商品名，用于词云图片命名
def get_goods_name(path):
    """
    提取csv文件路径中的商品名
    :param path: csv文件路径
    :return:
    """
    goods_name = path.split('-')[-2]
    return goods_name


# 读取停用词
def read_stopwords(path):
    """
    读取停用词
    :param path: sopwords文件路径
    :return:
    """
    f = open(path, "r", encoding='utf-8')
    stopwords = {}.fromkeys(f.read().split("\n"))
    f.close()
    return stopwords


# 读取csv文件,并切词
def cut_word(path, stopwords):
    """
    读取csv文件，使用jieba分词进行切词，对切词结果进行排序，
    提取出现频率最高的200个词
    :param path: csv文件路径
    :param stopwords:
    :return: 返回排序前200的切词结果，dict格式
    """
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        text_dict = {}
        for i in reader:
            text = i[2]
            text_cut = jieba.cut(text)
            for j in text_cut:
                if j not in stopwords and j != ' ':
                    if j in text_dict:            # 构建切词结果的字典
                        text_dict[j] += 1         # 新出现的词语，频数设置为1
                    else:
                        text_dict.update({j: 1})  # 已存在的，频数+1

    # 对全部的切词结果进行排序
    text_dict_sort = sorted(text_dict.items(), key=lambda x: x[1], reverse=True)

    count = 0
    cloud_text = ''
    for k, v in text_dict_sort:  # 截取排序前200的词语
        cloud_text += ' ' + k
        if count >= 200:
            break

    return cloud_text


# 制作词云
def make_cloud(cloud_text, image_path, goods_name):
    """
    根据词语文本和指定图片，绘制词云，以商品名命名
    :param cloud_text:
    :param image_path:
    :param goods_name:
    :return: 无
    """
    mask = np.array(image.open(image_path))
    wordcloud = WordCloud(
        mask=mask,
        background_color="white",
        max_font_size=150,
        max_words=200,
        font_path=".data/FZYTK.TTF").generate(cloud_text)

    image_produce = wordcloud.to_image()
    wordcloud.to_file('{0}.png'.format(goods_name))
    image_produce.show()


if __name__ == '__main__':
    text_path = './data/2019-10-12-长袖t恤男韩版秋季修身学生秋装男打底衫薄款上衣男衣服潮流-淘宝.csv'
    # text_path = './data/2019-10-13-飞利浦挂烫机家用GC617手持挂式蒸汽小型熨斗烫衣服熨烫机大功率-天猫.csv'
    stopwords_path = './data/stopwords.txt'
    image_path = './data/2333.jpg'

    goods_name = get_goods_name(text_path)
    stopwords = read_stopwords(stopwords_path)
    cloud_text = cut_word(text_path, stopwords)
    make_cloud(cloud_text, image_path, goods_name)


