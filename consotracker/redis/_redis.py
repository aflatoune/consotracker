import redis


class Redis:
    def __init__(self, host='localhost', port=6379, db=0):
        self.api = redis.StrictRedis(host=host, port=port, db=db)
