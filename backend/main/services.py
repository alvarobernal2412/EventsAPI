# File for consuming external APIs
import requests
from datetime import datetime

key = 'a0jJ7zlYgnA6EZhtn9G3avV5nAWz1Ofq' #Key for Accuweather API

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

#Function to get city key in accuweather api
def get_city_id(city_name, params={}):
    response = generate_request('http://dataservice.accuweather.com/locations/v1/cities/search?apikey='
                                + key + '&q='+ city_name, params)
    if response:
       city = response[0]
       return city['Key']


#Function to get an iconic phrase in accuweather api
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


#Function to get global events from CityEventsAPI
def get_global_events():
    response = generate_request('https://city-events-api.ew.r.appspot.com/api/events')
    if response:
        return response


#Function to create global events in CityEventsAPI
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
        return (response.status_code,response.json())

#Function to delete global events in CityEventsAPI
def delete_global_events(id):
    response = requests.delete('https://city-events-api.ew.r.appspot.com/api/events'+"/"+id+"/")
    if response:
        print(response.status_code)
        return response.status_code


#Function to get an event form CityEventsAPI
def get_global_events_id(id):
    response = generate_request('https://city-events-api.ew.r.appspot.com/api/events'+"/"+id+"/")
    if response:
        return response


'''
if __name__ == "__main__":
    
    #post_global_event("NewEvent5", "NewEvent5 desc", "Me", "Try", "Seville", "2022-05-23")
    delete_global_events("e21")
    #get_global_events_id("e29")
'''