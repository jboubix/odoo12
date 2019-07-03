
from datetime import datetime, timedelta, date
from workalendar.america import Mexico
# sudo pip3 install workalendar


def sub_business_days(from_date):
    holydaysmex = Mexico()
    current_date = from_date
    weekday = current_date.weekday()
    while weekday >= 5 or not holydaysmex.is_working_day(current_date):
        current_date -= timedelta(days=1)
        weekday = current_date.weekday()
    return current_date


def add_business_days(from_date, add_days):
    holydaysmex = Mexico()
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5 or not holydaysmex.is_working_day(current_date): # sunday = 6 and Holydays
            continue
        business_days_to_add -= 1
    return current_date


def next_business_day(from_date):
    holydaysmex = Mexico()
    current_date = from_date
    weekday = current_date.weekday()
    while weekday >= 5 or not holydaysmex.is_working_day(current_date):
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
    return current_date
