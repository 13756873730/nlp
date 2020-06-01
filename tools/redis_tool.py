import redis

r = redis.Redis(
    host='47.94.84.81', port=6379, db=0, password='123456',
    decode_responses=True
)


def keys():
    return r.keys()


def set(key, value, time=None):
    if time is None:
        r.set(key, value)
    else:
        r.setex(key, value, time)


def get(key):
    return r.get(key)


def delete(key):
    r.delete(key)


if __name__ == '__main__':
    print(r.keys())
    pass
