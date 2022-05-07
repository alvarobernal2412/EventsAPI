# File for consuming AccuWeather API
import requests

key = 'a0jJ7zlYgnA6EZhtn9G3avV5nAWz1Ofq'

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_city(q, params={}):
    response = generate_request('http://dataservice.accuweather.com/locations/v1/cities/search?apikey='
                                + key + '&q='+ q, params)
    if response:
       city = response[0]
       print(city)
       return city

def get_weather_1day(city_id, params={}):
    response = generate_request('http://dataservice.accuweather.com/forecasts/v1/daily/1day/' 
                                + city_id + '?apikey=' + key, params)
    if response:
        weather_1day = response
        print(weather_1day)
        return weather_1day

if __name__ == "__main__":
    get_city('Seville')
    # get_weather_1day('306733')
