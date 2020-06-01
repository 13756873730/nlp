import tools.data_tool as data
import jieba
import gensim
from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

"""
    Task-2 Word2Vector
        Word2Vector —— gensim.models.Word2Vec
        形成词汇表 —— model.wv.vocab
        计算两个词的相似度/相关程度 —— model.wv.similarity(word1, word2)
        计算与指定词语的最相关的词的列表 —— model.wv.most_similar(positive=word, topn=10)
        寻找对应关系 —— model.wv.most_similar(['球迷', '知道'], ['我'], topn=10)
        寻找集合中与其他词相关性最差的一个 —— model.wv.doesnt_match(['曼城', '皇马', '尤文', '中超'])
"""


# 加载数据
def load_data():
    news_list = data.random_news(size=2000, seed=None)
    words_list = []
    for news in news_list:
        words = jieba.lcut(sentence=news.content, cut_all=False, HMM=True)
        words_list.extend(words)
    open('../resource/random_news_content.txt', 'w', encoding='UTF-8').write(' '.join(words_list))


if __name__ == '__main__':
    # 加载数据
    # load_data()
    print('数据加载完毕...')
    print('---------------------------------------------------')

    # 加载语料
    corpus = word2vec.Text8Corpus('../resource/random_news_content.txt')
    print('语料加载完毕...')
    print('---------------------------------------------------')

    # 创建模型
    w2v_model = gensim.models.Word2Vec(
        sentences=corpus,
        size=200, window=20, min_count=2, workers=10
    )
    print('模型创建完毕...')
    # 训练模型
    # w2v_model.train(
    #     sentences=corpus,
    #     total_examples=corpus.max_sentence_length,
    #     epochs=10
    # )
    # print('模型训练完毕...')
    print('---------------------------------------------------')

    # 形成词汇表
    vocabulary_list = w2v_model.wv.vocab
    print('词汇表中共有{}个词汇。'.format(len(vocabulary_list)))
    print(''.join(['{}-{}'.format(key, value) for key, value in vocabulary_list.items()]))
    print('---------------------------------------------------')

    # 计算两个词的相似度/相关程度
    word1 = '转会'
    word2 = '租借'
    words_similarity = w2v_model.wv.similarity(word1, word2)
    print('【{}】和【{}】两个词语相关程度为{}。'.format(word1, word2, words_similarity))
    print('---------------------------------------------------')

    # 计算与指定词语的最相关的词的列表
    word = '球迷'
    most_similar_words = w2v_model.wv.most_similar(positive=word, topn=10)
    for similar_word, degree in most_similar_words:
        print(similar_word, degree)
    print('---------------------------------------------------')

    # 寻找对应关系
    predict_word_list = w2v_model.wv.most_similar(['球迷', '知道'], ['我'], topn=10)
    for predict_word, degree in most_similar_words:
        print(predict_word, degree)
    print('---------------------------------------------------')

    # 寻找集合中与其他词相关性最差的一个
    predict_word = w2v_model.wv.doesnt_match(['曼城', '皇马', '尤文', '中超'])
    print(predict_word)
    print('---------------------------------------------------')

    # train model
    # w2v_model.train(
    #     sentences=content,
    #     total_examples=len(content),
    #     epochs=10
    # )

    # test
    # word = '亿'
    # predict = w2v_model.wv.most_similar(positive=word, topn=10)
    # print(predict)
    pass
