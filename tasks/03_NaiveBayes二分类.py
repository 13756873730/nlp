import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from tools import data_tool as data
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import jieba

"""
    Task-3 二分类任务
        依据新闻是否为国内新闻，进行二分类（Foreign/0、China/1）
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
    return word_list


# 文本处理，也就是样本生成过程
def preprocessing(path, test_size=0.2, max_count=10000):
    # 指定文件夹下，分类文件夹列表
    class_folder_list = os.listdir(path)
    X = []  # data
    y = []  # label
    # 遍历分类文件夹
    for folder in class_folder_list:
        class_folder_path = os.path.join(path, folder)
        file_list = os.listdir(class_folder_path)
        # 遍历分类文件夹下的所有文件
        index = 1
        for file in file_list:
            if index > max_count:  # TODO 防止内存溢出
                break
            content = open(os.path.join(class_folder_path, file), 'r', encoding='UTF-8').read()
            # jieba分词
            word_list = cut_word(sentence=content, parallel=False)
            X.append(word_list)  # 训练集数据（列表的列表）
            y.append(folder)  # 类别列表
            index += 1

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=666)

    # 统计词频
    counter = Counter()  # 统计词频
    for word_list in X_train:
        counter.update(word_list)
    dictionary = [key for key, count in counter.most_common()]
    return dictionary, X_train, X_test, y_train, y_test


# 停用词set集合
def get_stopwords_set(path):
    return set([line.strip() for line in open(path, 'r', encoding='UTF-8').readlines()])


# 选取特征词
def get_feature_words(dictionary, space_index, stopwords, max_dim=1000):
    feature_words = []
    n = 1
    for t in range(space_index, len(dictionary), 1):
        if n > max_dim:  # 取dictionary中dim=max_dim做为文本特征
            break
        # 特征词不能为数字、不能在停用词中、且特征词长度在[2, 4]之间
        if (not dictionary[t].isdigit()) and (dictionary[t] not in stopwords) and (2 <= len(dictionary[t]) <= 4):
            feature_words.append(dictionary[t])
            n += 1
    return feature_words


# 提取文本特征
def get_sentence_features(sentence, feature_words):
    text_words = set(sentence)
    features = [1 if word in text_words else 0 for word in feature_words]
    return features


# 预测
def predict(X_train_feature_words, y_train, X_predict_feature_words):
    nb_clf = MultinomialNB()
    nb_clf.fit(X=X_train_feature_words, y=y_train)
    y_predict = nb_clf.predict(X_predict_feature_words)
    return y_predict


if __name__ == '__main__':
    # 文本预处理
    articles_path = '../resource/articles_binary_classifier'
    dictionary, X_train, X_test, y_train, y_test = preprocessing(
        path=articles_path,
        max_count=1000
    )
    print(len(dictionary), len(X_train), len(X_test), len(y_train), len(y_test))
    print(y_train[:10])
    print(y_test[:10])
    print('dictionary len={}'.format(len(dictionary)))

    # 生成stopwords_set
    stopwords_path = '../resource/ChineseStopwords.txt'
    stopwords = get_stopwords_set(path=stopwords_path)
    print('stopwords len={}'.format(len(stopwords)))

    # 模型最优参数
    max_dim = 1000
    best_nb_clf, best_score = None, 0
    print("start")
    # 文本特征提取和分类
    accuracy_score_list = []
    split_space = range(0, max_dim, 20)  # 目的是寻找最优参数
    for space_index in split_space:
        # 选取特征词
        feature_words = get_feature_words(
            dictionary=dictionary,
            space_index=space_index,
            stopwords=stopwords,
            max_dim=max_dim
        )
        print(space_index, feature_words)

        # 提取文本特征
        X_train_feature_words = [get_sentence_features(sentence, feature_words) for sentence in X_train]
        X_test_feature_words = [get_sentence_features(sentence, feature_words) for sentence in X_test]

        # 评价分类算法
        nb_clf = MultinomialNB()
        nb_clf.fit(X=X_train_feature_words, y=y_train)
        accuracy_score = nb_clf.score(X=X_test_feature_words, y=y_test)
        best_nb_clf = nb_clf if accuracy_score > best_score else best_nb_clf
        accuracy_score_list.append(accuracy_score)
    print(accuracy_score_list)

    # 找到最好的结果
    best_index = accuracy_score_list.index(max(accuracy_score_list))
    print(best_index, split_space[best_index], accuracy_score_list[best_index])

    # 结果评价
    plt.plot(split_space, accuracy_score_list)
    plt.title('split_space and test_accuracy')
    plt.xlabel('split_space')
    plt.ylabel('test_accuracy')
    plt.show()
    print("finished")

    # 预测新数据
    while True:
        # 随机输入数据
        news = data.random_news()
        # 分词
        X_predict = cut_word(sentence=news.content, parallel=False)
        # 选取特征词
        feature_words = get_feature_words(
            dictionary=dictionary,
            space_index=best_index,
            stopwords=stopwords,
            max_dim=max_dim
        )
        # 提取文本特征
        X_predict_feature_words = [get_sentence_features(sentence=X_predict, feature_words=feature_words)]
        # 预测
        y_predict = best_nb_clf.predict(X_predict_feature_words)
        print(news.content)
        China_type = {0: 'Foreign', 1: 'China'}
        print('y_true={}'.format(China_type[news.china_type]), 'y_predict={}'.format(y_predict[0]))
    pass
