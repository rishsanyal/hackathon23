import redis
import json
from redis_worker import redis_db
from mock import mock_student_queue

# Connect to Redis
# redis_client = redis.Redis(host='redis', port=6379, db=0)

# Define the name of the queue
QUEUE_NAME = 'oh_student_queue'

# Get the next item from the queue
# next_item = redis_client.rpop(queue_name)
# print(next_item.decode())

# QUEUE CRUD
def populate_queue(queue_name=QUEUE_NAME) -> None:
    redis_db.flushdb()
    for user in mock_student_queue.USER_INFO:
        redis_db.lpush(queue_name, json.dumps(user))
        

def print_test() -> None:
    """Test function to print mock data.
    """
    print(mock_student_queue.USER_INFO)


def get_students_queue(queue_name=QUEUE_NAME) -> list:
    """Get the current queue of students.

    Args:
        queue_name (str, optional): Name of the queue. Defaults to QUEUE_NAME.
    """
    return redis_db.lrange(queue_name, 0, -1)


def update_students_queue(user_id: str, queue_name=QUEUE_NAME) -> None:
    """Update the queue of students. Add a student to the queue.

    Args
        user_id (str): ID of the student to add to the queue.
    """
    curr = None
    for i in mock_student_queue.USER_INFO:
        if i['user_id'] == user_id:
            curr = i
            break
    if curr is None:
        raise ValueError('User not found')
    redis_db.lpush(queue_name, json.dumps(curr))


def delete_students_queue(user_id: str, queue_name=QUEUE_NAME) -> None:
    """Delete a student from the queue.

    Args:
        user_id (str): ID of the student to delete from the queue.
    """
    curr = None
    for i in redis_db.lrange(queue_name, 0, -1):
        dict_obj = json.loads(i)
        if dict_obj['user_id'] == user_id:
            curr = dict_obj
            break
    if curr is None:
        raise ValueError('User not found')
    redis_db.lrem(queue_name, 0, json.dumps(curr))
