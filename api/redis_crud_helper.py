from redis_worker import redis_db

USERINFO_QUEUE = "userinfo_"

def get_student_name_from_id(user_id: int) -> str:
    """Get student name from user id.

    Args:
        user_id (int): User id
    """

    # Get student name from redis given a user_id

    return redis_db.get(USERINFO_QUEUE + f'{user_id}').decode('utf-8')

def add_student_info(user_id: int, username: str) -> None:
    """Add student info to redis.

    Args:
        user_id (int): User id
        full_name (str): Student full name
    """

    # Add student info to redis
    redis_db.set(USERINFO_QUEUE + f'{user_id}', username)