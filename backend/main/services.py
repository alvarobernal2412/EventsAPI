# File for consuming AccuWeather API
import requests
import json

key = 'm4IWCaABNGfRD0fGdJPCcshMKTrlomQV'

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_city_id(city_name, params={}):
    response = generate_request('http://dataservice.accuweather.com/locations/v1/cities/search?apikey='
                                + key + '&q='+ city_name, params)
    if response:
       city = response[0]
       aux = json.dumps(city) # Convierte a str
       city_json = json.loads(aux) # Convierte a dict
       return city_json['Key']

def get_weather_1day(city, params={}):
    response = generate_request('http://dataservice.accuweather.com/forecasts/v1/daily/1day/' 
                                + str(get_city_id(city)) + '?apikey=' + key, params)
    if response:
        weather_1day = response
        aux = json.dumps(weather_1day)
        weather_1day_json =  json.loads(aux)
        print(weather_1day['DailyForecasts'])
        return weather_1day

if __name__ == "__main__":
    get_weather_1day('Seville')
