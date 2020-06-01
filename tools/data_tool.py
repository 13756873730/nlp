import json
import datetime
import random
from tools.crawler_tool import FootballNews
import tools.crawler_tool as crawler
import tools.mysql_tool as mysql
import tools.redis_tool as redis
import os


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime(crawler.datetime_format)


def encoder(news):
    dictionary = {
        'id': news.id,
        'serial_number': news.serial_number,
        'create_time': news.create_time,
        'news_type': news.news_type,
        'china_type': news.china_type,
        'tags': news.tags,
        'title': news.title,
        'content': news.content
    }
    news_str = str(dictionary)
    return news_str


def decoder(news_str):
    dictionary = eval(news_str)
    return FootballNews(
        id=dictionary['id'],
        serial_number=dictionary['serial_number'],
        create_time=dictionary['create_time'],
        news_type=dictionary['news_type'],
        china_type=dictionary['china_type'],
        tags=dictionary['tags'],
        title=dictionary['title'],
        content=dictionary['content']
    )


def random_news(size=1, seed=None):
    if seed is not None:
        random.seed(seed)
    key_list = redis.keys()
    news_list = []
    for _ in range(size):
        random_index = random.randint(a=0, b=len(key_list))
        news_str = redis.get(key=key_list[random_index])
        news = decoder(news_str=news_str)
        news_list.append(news)
    return news_list[0] if size == 1 else news_list


def select_from_redis(id):
    news_str = redis.get(key=id)
    news = decoder(news_str=news_str)
    return news


def user_mysql_refresh_redis(start_index):
    for index in range(start_index):
        news_list = mysql.select(serial_number=index)
        print(news_list)
        if len(news_list) != 0:
            news = news_list[0]
            redis.set(key=news.id, value=encoder(news=news))
    print('finish...', len(redis.keys()))


def write2articles4binary():
    China_path = '../resource/articles_binary_classifier/China'
    Foreign_path = '../resource/articles_binary_classifier/Foreign'
    keys = redis.keys()
    for key in keys:
        count1 = len(os.listdir(China_path))
        count2 = len(os.listdir(Foreign_path))
        count = count1 + count2
        print(count1, count2, count)
        if count >= 4000:
            break
        news = redis.get(key)
        news = decoder(news)
        write_path = (China_path if news.china_type == 1 else Foreign_path) + '/{}.txt'
        open(file=write_path.format(news.serial_number), mode='w', encoding='UTF-8').write(news.content)


def write2articles4multi():
    path = '../resource/articles_multi_classifier/'
    keys = redis.keys()
    for key in keys:
        count1 = len(os.listdir((path + '1')))
        count2 = len(os.listdir((path + '2')))
        count3 = len(os.listdir((path + '3')))
        count4 = len(os.listdir((path + '4')))
        count5 = len(os.listdir((path + '5')))
        count6 = len(os.listdir((path + '6')))
        count = count1 + count2 + count3 + count4 + count5 + count6
        print(count, count1, count2, count3, count4, count5, count6)
        if count >= 4000:
            break
        news = redis.get(key)
        news = decoder(news)
        write_path = path + str(news.news_type) + '/{}.txt'
        open(file=write_path.format(news.serial_number), mode='w', encoding='UTF-8').write(news.content)


if __name__ == '__main__':
    # user_mysql_refresh_redis(start_index=5000)
    write2articles4multi()
    # write2articles4binary()
    pass
