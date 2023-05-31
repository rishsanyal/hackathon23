import redis
import json

from redis_worker import redis_db
from redis_crud_helper import get_student_name_from_id, add_student_info
from mock import mock_student_queue

# Connect to Redis
# redis_client = redis.Redis(host='redis', port=6379, db=0)

# Define the name of the queue
QUEUE_NAME = 'oh_student_queue'
OH_TURN_NOTIFICATION = 'oh_turn_notification_'
OH_STUDENT_QUEUE = 'oh_student_queue_'

# Get the next item from the queue
# next_item = redis_client.rpop(queue_name)
# print(next_item.decode())

# QUEUE CRUD
def populate_user_info_queue(queue_name=QUEUE_NAME) -> None:
    """Populate the queue with mock data."""

    redis_db.flushdb()
    for user in mock_student_queue.USER_INFO:
        redis_db.lpush(queue_name, json.dumps(user))
        add_student_info(int(user['user_id']), user['user_name'])

# TEST FUNCTIONS ##

def print_user_info_queue(queue_name=QUEUE_NAME) -> None:
    """Print the queue."""
    print(redis_db.lrange(queue_name, 0, -1))

def clear_user_info_queue(queue_name=QUEUE_NAME) -> None:
    """Clear the queue."""
    redis_db.flushdb()
    populate_user_info_queue()
    print_user_info_queue()

def print_test() -> None:
    """Test function to print mock data."""
    print(mock_student_queue.USER_INFO)

## OFFICE HOURS RELATED FUNCTIONS

def get_students_oh_queue(office_hours_id: int, queue_name=OH_STUDENT_QUEUE) -> list:
    # """Get the current queue of students for an OH session.

    # Args:
    #     queue_name (str, optional): Name of the queue. Defaults to QUEUE_NAME.
    # """
    student_ids = redis_db.lrange(queue_name+f"{office_hours_id}", 0, -1)

    student_names = []

    for student_id in student_ids:
        student_name = get_student_name_from_id(student_id)
        student_names.append(student_name)

    return student_names

def add_student_to_oh_queue(user_id: str, office_hours_id: int, queue_name=OH_STUDENT_QUEUE) -> None:
    """Update the queue of students. Add a student to the queue."""

    curr = None
    # for i in mock_student_queue.USER_INFO:
    #     if i['user_id'] == user_id:
    #         curr = i
    #         break
    # if curr is None:
    # #     raise ValueError('User not found')
    # redis_db.lpush(OH_STUDENT_QUEUE + , json.dumps(curr))

    redis_db.lpush(queue_name + f'{office_hours_id}', user_id)


def delete_student_from_oh_queue(office_hours_id: int, queue_name=QUEUE_NAME) -> int:
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

    return(redis_db.lrem(queue_name + f'{office_hours_id}', 0, json.dumps(curr)))

def add_student_notification_office_hours(user_id: int, class_id: int, office_hour_id: int):
    """Add a student to the notification list for office hours.

    Args:
        user_id (str): ID of the student to add to the notification list.
        class_id (str): ID of the class to add to the notification list.
    """
    redis_db.sadd(f'oh_notification_{class_id}_{office_hour_id}', user_id)

def remove_student_notification_office_hours(user_id: int, class_id: int, office_hour_id: int):
    """Remove a student from the notification list for office hours.

    Args:
        user_id (str): ID of the student to remove from the notification list.
        class_id (str): ID of the class to remove from the notification list.
    """
    redis_db.srem(f'oh_notification_{class_id}_{office_hour_id}', user_id)


def add_student_notification_office_hours_turn(user_id: int, class_id: int, office_hour_id: int):
    """Add a student to the notification list for office hours turn.

    Args:
        user_id (str): ID of the student to add to the notification list.
        class_id (str): ID of the class to add to the notification list.
    """
    redis_db.sadd(OH_TURN_NOTIFICATION + f'{class_id}_{office_hour_id}', user_id)

def remove_student_notification_office_hours_turn(user_id: int, class_id: int, office_hour_id: int):
    """Remove a student from the notification list for office hours turn.

    Args:
        user_id (str): ID of the student to remove from the notification list.
        class_id (str): ID of the class to remove from the notification list.
    """
    redis_db.srem(OH_TURN_NOTIFICATION + f'{class_id}_{office_hour_id}', user_id)

def get_all_student_notification_office_hours():
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


def get_office_hours_students_queue(office_hour_id: int):
    """Get the current queue of students for an OH session.

    Args:
        queue_name (str, optional): Name of the queue. Defaults to QUEUE_NAME.
    """
    return redis_db.lrange(OH_STUDENT_QUEUE + f'{office_hour_id}', 0, -1)
