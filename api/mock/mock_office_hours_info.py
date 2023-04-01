from datetime import datetime, timedelta

zoom_link = "https://zoom.us/j/123456789"

# Get the current time in UTC and format it as an ISO 8601 string
curr_time_obj = datetime.utcnow()
time_string = curr_time_obj.isoformat(timespec='seconds') + 'Z'

# Get the current date in UTC and format it as an ISO 8601 string
curr_date_obj = datetime.utcnow().date()
date_string = curr_date_obj.isoformat()

# Create timedelta objects for adding 24 hours and 3 days
one_day = timedelta(days=1)
three_days = timedelta(days=3)

# Increment time by 24 hours
new_time_obj = curr_time_obj + one_day

# Increment date by 3 days
new_date_obj = curr_date_obj + three_days

MOCK_OFFICE_HOURS_INFO = {
    "office_hours_info": [
        [
            { "join": True },
            { "time": str(new_time_obj).split(" ")[1]},
            { "date": new_date_obj.isoformat()},
            { "zoom": zoom_link}
        ],
        [
            { "join": True },
            { "time": str(new_time_obj).split(" ")[1]},
            { "date": (new_date_obj + three_days).isoformat()},
            { "zoom": zoom_link}
        ],
        [
            { "join": True },
            { "time": str(new_time_obj).split(" ")[1]},
            { "date": (new_date_obj + three_days + three_days).isoformat()},
            { "zoom": zoom_link}
        ]
    ]
}
