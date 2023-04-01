import os

import redis
# from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')

# conn = redis.from_url(redis_url)
redis_db = redis.Redis(host='redis', port=6379, decode_responses=True)


# if __name__ == '__main__':
#     with Connection(conn):
#         worker = Worker(list(map(Queue, listen)))
#         worker.work()