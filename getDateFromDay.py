from datetime import date, timedelta

def next_weekday(weekday):

    # print('This is next_weekday of getDateFromDay.py')

    days = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    days_ahead = days[weekday] - date.today().weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (date.today() + timedelta(days_ahead))
