from requests_html import HTMLSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, NVARCHAR, Integer, DateTime, VARCHAR, Text
from sqlalchemy.orm import sessionmaker
import uuid
import datetime
import threading
import threadpool
import pymysql

pymysql.install_as_MySQLdb()

# 创建对象的基类:
Base = declarative_base()


class FootballNews(Base):
    __tablename__ = 'FOOTBALL_NEWS'

    id = Column(name='ID', type_=NVARCHAR(36), primary_key=True)
    serial_number = Column(name='SERIAL_NUMBER', type_=Integer, unique=True)
    create_time = Column(name='CREATE_TIME', type_=DateTime, nullable=False)
    news_type = Column(name='NEWS_TYPE', type_=Integer, nullable=False)
    china_type = Column(name='CHINA_TYPE', type_=Integer, nullable=False)
    tags = Column(name='TAGS', type_=VARCHAR(255))
    title = Column(name='TITLE', type_=VARCHAR(255), nullable=False)
    content = Column(name='CONTENT', type_=Text, nullable=False)

    def __repr__(self):
        return 'id={}, serial_number={}, create_time={}, news_type={}, china_type={}, tags={}, title={}, content={}' \
            .format(self.id, self.serial_number, self.create_time, self.news_type,
                    self.china_type, self.tags, self.title, self.content)


# url
football_news_url = 'http://www.tzuqiu.cc/news/{}/show.do?fancybox=true'
# path
local_file_path = './Football_news_{}.html'
# datetime format
datetime_format = '%Y-%m-%d %H:%M:%S'
# thread pool size
thread_pool_size = 8
# Enum: news_type
news_type_dictionary = {
    '转会': 1,
    '转会流言': 2,
    '统计': 3,
    '球员动态': 4,
    '球队动态': 5,
    '球员身价': 6
}
lock = threading.Lock()


def crawler_and_save(serial_number, save=False):
    # Send
    lock.acquire()  # TODO
    session = HTMLSession()
    response = session.get(url=football_news_url.format(serial_number))
    session.close()
    lock.release()  # TODO

    # Fail
    if response.status_code != 200:
        result = None

    # Success
    page_text = response.text

    # Save
    if save:
        with open(local_file_path.format(serial_number), 'w', encoding='UTF-8') as file:
            file.write(page_text)

    news = FootballNews(id=str(uuid.uuid4()).upper(), serial_number=serial_number, news_type=0)
    # Analyse
    try:
        area = response.html.find('.new-area')[0]
        news.news_type = news_type_dictionary.get(area.find('span')[0].text.strip())
        try:
            news.create_time = datetime.datetime.strptime(area.find('span')[1].text[6:].strip(), datetime_format)
        except Exception as e:
            news.create_time = datetime.datetime.now()
        news.title = area.find('.new-title')[0].text.strip()
        news.content = ''
        for p in area.find('.new-content')[0].find('p'):
            news.content = news.content + p.text.strip()
        news.tags = []
        for a in area.find('.new-tags')[0].find('a'):
            news.tags.append(a.text.strip())
        news.tags = ','.join(news.tags)
    except Exception as e:
        news = None

    def get_session():
        # 初始化数据库连接:
        engine = create_engine('mysql://root:123456@47.94.84.81:3306/test_mysql')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建session对象:
        session = DBSession()
        return session

    def close_session(session):
        session.close()

    if news is not None:
        try:
            session = get_session()
            session.add(news)
            session.commit()
            close_session(session)
            print('serial_number={}，写入完毕！'.format(serial_number))
        except Exception as e:
            print('serial_number={}，Error: 向MySQL写入数据失败！'.format(serial_number))
    else:
        print('serial_number={}，Error: 当前页面不存在！'.format(serial_number))


def execute(start_index, end_index):
    pool = threadpool.ThreadPool(num_workers=thread_pool_size)
    params = [index for index in range(start_index, end_index)]
    requests = threadpool.makeRequests(crawler_and_save, params)
    [pool.putRequest(req) for req in requests]
    pool.wait()


if __name__ == '__main__':
    # execute(4971, 10000)
    pass
