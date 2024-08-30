from fastapi import FastAPI 
import datetime
import re
import csv

app = FastAPI()

# accepted format: "DD-MM-YYYY:HH:MM"
DATE_TIME_FORMAT = "%d-%m-%Y:%H:%M"
DAYS = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]

@app.get("/")
def root():
    return "Follow this format when inputting a date and time: DD-MM-YYYY:HH:MM"

@app.get("/restaurants")
def get_opening_times(date_and_time):
    formatted_date = datetime.datetime.strptime(date_and_time, DATE_TIME_FORMAT)
    try:
        return get_restaurants_from_csv(formatted_date)
    except Exception as e:
        return e

def get_restaurants_from_csv(date: datetime.datetime):
    results = []
    with open("restaurants.csv", mode="r") as file:
        csv_read = csv.reader(file)
        next(file)  # skip header
        for line in csv_read:
            opening_hours = line[1].split("/")
            for time in opening_hours:
                day_range, start_time, end_time = parse_opening_times(time)
                day = date.weekday()  # returns int for each day. Mon=0, Sun=6
                if not is_in_day_range(day, day_range):
                    continue
                if start_time <= date.time() <= end_time:
                    print(line[0], day_range, start_time, end_time)
                    results.append(line[0])
    return results

def format_time(time_string):
    if ":" in time_string:
        return datetime.datetime.strptime(time_string, "%I:%M %p").time()
    return datetime.datetime.strptime(time_string, "%I %p").time()

def parse_opening_times(opening_times):
    pattern = r'([A-Za-z-,\s]+)\s+(\d{1,2}:\d{2} [apmAPM]{2}|\d{1,2} [apmAPM]{2})\s*-\s*(\d{1,2}:\d{2} [apmAPM]{2}|\d{1,2} [apmAPM]{2})'
    match = re.match(pattern, opening_times)
    if match:
        day_range = match.group(1)
        start_time = format_time(match.group(2))
        end_time = format_time(match.group(3))
        return day_range, start_time, end_time

def is_in_day_range(day, day_range):
    open_days = day_range.split(",")
    for range in open_days:
        if '-' not in range:
            if day == DAYS.index(range.strip()):
                return True
            return False
        start_day, end_day = range.strip().split('-')
        start_day_index = DAYS.index(start_day)
        end_day_index = DAYS.index(end_day)
        print(DAYS[day], DAYS[start_day_index:end_day_index])
        if DAYS[day] in DAYS[start_day_index:end_day_index]:
            return True

