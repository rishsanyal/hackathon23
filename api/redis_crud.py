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
    """Populate the queue with mock data."""

    redis_db.flushdb()
    for user in mock_student_queue.USER_INFO:
        redis_db.lpush(queue_name, json.dumps(user))


def print_test() -> None:
    """Test function to print mock data."""
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

def add_student_notification_office_hours(user_id: int, class_id: int, office_hour_id: int) -> None:
    """Add a student to the notification list for office hours.

    Args:
        user_id (str): ID of the student to add to the notification list.
        class_id (str): ID of the class to add to the notification list.
    """
    redis_db.sadd(f'oh_notification_{class_id}_{office_hour_id}', user_id)

def remove_student_notification_office_hours(user_id: int, class_id: int, office_hour_id: int) -> None:
    """Remove a student from the notification list for office hours.

    Args:
        user_id (str): ID of the student to remove from the notification list.
        class_id (str): ID of the class to remove from the notification list.
    """
    redis_db.srem(f'oh_notification_{class_id}_{office_hour_id}', user_id)

def get_all_student_notification_office_hours() -> dict:
    """Get the notification status of a student for office hours.

    Args:
        user_id (str): ID of the student to get the notification status.
        class_id (str): ID of the class to get the notification status.

    Returns:
        bool: True if the student is in the notification list, False otherwise.
    """
    office_hours_list = []
    redis_keys = redis_db.keys('oh_notification_*')

    for key in redis_keys:
        print(key)
        print(redis_db.smembers(key))
        office_hours_list.extend(redis_db.smembers(key))

    return office_hours_list


