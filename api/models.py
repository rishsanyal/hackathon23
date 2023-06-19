# This is where we crate models for the following uses:
# - Class
#   - Class Name
#   - Professor? Maybe later

# - Office Hours
#   - Class
#   - Professor/OH Conductor
#   - ID of OH for Redis Queue (The queue will reset after every termination time of class)
#   - Start time
#   - End time
#   - Day of week


# - Then we create a Mock Class and Mock Office Hours for testing purposes.
# - We link the class to a User and link the mock Class object to a OH obj
# - We create a Redis Queue for the OH on every session start.
# - We clear the Redis Queue for the OH on every session end.
# - We add user name viewing capability from the redis queue.

