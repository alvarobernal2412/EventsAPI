# File for consuming AccuWeather API
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
                print(weather['DailyForecasts'][days_diff]['Night']['IconPhrase'])
                return str(weather['DailyForecasts'][days_diff]['Night']['IconPhrase'])
            else:
                print(weather['DailyForecasts'][days_diff]['Day']['IconPhrase'])
                return str(weather['DailyForecasts'][days_diff]['Day']['IconPhrase'])

if __name__ == "__main__":
    get_weather("Seville", "2022-05-20", "15:00:00")
    
