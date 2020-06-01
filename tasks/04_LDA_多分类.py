import jieba
import gensim
import numpy as np
from tools import data_tool as data

"""
    Task-4 多分类任务
"""


# jieba分词
def cut_word(sentence, parallel=False, processnum=2):
    if parallel:
        # 开启并行分词模式，参数为并行进程数，不支持windows
        jieba.enable_parallel(processnum=processnum)
        word_list = jieba.lcut(sentence, cut_all=False, HMM=True)
        # 关闭并行分词模式
        jieba.disable_parallel()
    else:
        word_list = jieba.lcut(sentence, cut_all=False, HMM=True)
    # 去除停用词
    stopwords = [
        line.strip() for line in open(
            file='../resource/ChineseStopwords.txt',
            mode='r',
            encoding='UTF-8'
        ).readlines()
    ]
    new_word_list = []
    for word in word_list:
        if not stopwords.__contains__(word):
            new_word_list.append(word)
    return new_word_list


# 文本预处理
def preprocessing(article_size=4000):
    article_count = 0
    X = []
    news_list = data.random_news(size=article_size)
    for news in news_list:
        content = news.content
        word_list = cut_word(sentence=content, parallel=False)
        X.append(word_list)
    return np.array(X)


if __name__ == '__main__':
    X = preprocessing(article_size=300)

    dictionary = gensim.corpora.Dictionary(X)
    corpus = [dictionary.doc2bow(text) for text in X]
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    num_topics = 3
    lda_model = gensim.models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)

    # topicno=1 转会，最相关的五个词
    print(lda_model.print_topic(topicno=1, topn=10))
    print('----------------------------------------------------')

    topic_list = lda_model.print_topics(num_topics=num_topics, num_words=10)
    for topic in topic_list:
        print(topic)

    # print(lda_model.get_document_topics(word_id))
    pass
