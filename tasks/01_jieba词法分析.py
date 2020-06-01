import tools.data_tool as data
import jieba
from jieba import posseg, analyse
from collections import Counter

"""
    Task-1 词法分析
        分词 —— jieba.lcut(sentence, cut_all=False, HMM=True)
        去除停用词 —— def remove_stopwords(words):
        自定义词典 —— jieba.load_userdict(file_name)
        词频统计 —— collections.Counter
        词性标注 —— jieba.analyse.posseg.cut
        关键词统计 —— jieba.analyse.tfidf | jieba.analyse.extract_tags
"""


# 去除停用词
def remove_stopwords(words):
    new_words = []
    stopwords = [
        line.strip() for line in open(
            file='../resource/ChineseStopwords.txt',
            mode='r',
            encoding='UTF-8'
        ).readlines()
    ]
    for word in words:
        if not stopwords.__contains__(word):
            new_words.append(word)
    return new_words


if __name__ == '__main__':
    # 获取一条随机数据
    news = data.random_news(size=1, seed=None)
    # news = data.select_from_redis(id='C7FF7586-236A-49EC-817B-E30EFC54A1AE')
    print(news)
    print('---------------------------------------------------')

    # 添加自定义词典
    jieba.load_userdict(f='../resource/my_dictionary.txt')
    print('加载自定义词典完成。')
    print('---------------------------------------------------')

    # 分词
    content = news.content
    print(content)
    words = jieba.lcut(sentence=content, cut_all=False, HMM=True)
    print('---------------------------------------------------')

    # 去除停用词
    words = remove_stopwords(words)
    print('/'.join(words))
    print('---------------------------------------------------')

    # 词频统计
    counter = Counter(words)
    print('/'.join(['{}*{}'.format(key, value) for key, value in counter.items()]))
    print('---------------------------------------------------')

    # 词性标注
    words = jieba.posseg.cut(sentence=content)
    print(''.join(['{}【{}】'.format(word, flag) for word, flag in words]))
    print('---------------------------------------------------')

    # 关键词抽取
    key_words = jieba.analyse.tfidf(sentence=content, topK=10, withWeight=True, allowPOS=())
    # key_words = analyse.extract_tags(sentence=content, topK=10, withWeight=True, allowPOS=())
    for key_word in key_words:
        print(key_word)
    print('---------------------------------------------------')

    pass
