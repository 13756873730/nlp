from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools.crawler_tool import FootballNews

# 初始化数据库连接:
engine = create_engine('mysql://root:123456@47.94.84.81:3306/test_mysql')


def select(id=None, serial_number=None, create_time=None, news_type=None,
           china_type=None, tags=None, title=None, content=None):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    query = session.query(FootballNews)
    if id is not None:
        query = query.filter(FootballNews.id.like('%{}%'.format(id)))
    if serial_number is not None:
        query = query.filter(FootballNews.serial_number == serial_number)
    if create_time is not None:
        query = query.filter(FootballNews.create_time.like('%{}%'.format(create_time)))
    if news_type is not None:
        query = query.filter(FootballNews.news_type.like('%{}%'.format(news_type)))
    if china_type is not None:
        query = query.filter(FootballNews.china_type.like('%{}%'.format(china_type)))
    if tags is not None:
        query = query.filter(FootballNews.tags.like('%{}%'.format(tags)))
    if title is not None:
        query = query.filter(FootballNews.title.like('%{}%'.format(title)))
    if content is not None:
        query = query.filter(FootballNews.content.like('%{}%'.format(content)))
    result = query.all()
    session.close()
    return result


def insert_or_update(news_list):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add_all(news_list)
        session.commit()
        return True
    except Exception as e:
        print('向MySQL插入数据失败！')
        return False


if __name__ == '__main__':
    news_list = select(china_type=1)
    print(len(news_list))
    pass
