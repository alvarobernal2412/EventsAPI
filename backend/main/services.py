# File for consuming AccuWeather API
import json
from turtle import pos
from urllib import response
import requests
from datetime import datetime

key = 'a0jJ7zlYgnA6EZhtn9G3avV5nAWz1Ofq'

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_city_id(city_name, params={}):
    response = generate_request('http://dataservice.accuweather.com/locations/v1/cities/search?apikey='
                                + key + '&q='+ city_name, params)
    if response:
       city = response[0]
       return city['Key']

def get_weather(city, date, time, params={}):
    response = generate_request('http://dataservice.accuweather.com/forecasts/v1/daily/5day/' 
                                + get_city_id(city) + '?apikey=' + key, params)

    date = datetime.strptime(date, "%Y-%m-%d")
    today = datetime.combine(datetime.today(), datetime.min.time())
    days_diff = (date-today).days
    
    time = datetime.strptime(time, "%X").time()
    night_start = datetime.strptime("21:00:00", "%X").time()
    night_end = datetime.strptime("6:00:00", "%X").time()

    if response:
        weather = response
        if  0 <= days_diff <= 4:
            if night_start <= time or time <= night_end:
                return str(weather['DailyForecasts'][days_diff]['Night']['IconPhrase'])
            else:
                return str(weather['DailyForecasts'][days_diff]['Day']['IconPhrase'])

def get_global_events():
    response = generate_request('https://city-events-api.ew.r.appspot.com/api/events')
    if response:
        return response

def post_global_event(name, description, organizer, category, location, date):
    response = requests.post('https://city-events-api.ew.r.appspot.com/api/events', 
        json={"name": name,
            "description": description,
            "organizer": organizer,
            "category": category,
            "location": location,
            "date": date           
            })
    if response:
        return (response.status_code, response.json())

        

if __name__ == "__main__":
    # get_global_events()
    post_global_event("NewEvent5", "NewEvent5 desc", "Me", "Try", "Seville", "2022-05-23")


    
