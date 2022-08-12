import requests


def get_weather_status(data):
    weather_status_en = data['weather'][0]['main']
    weather_status_ru = {
        'Clouds': 'облачно',
        'Drizzle': 'морось',
        'Rain': 'дождь',
        'Snow': 'снег',
        'Clear': 'чистое небо',
        'Thunderstorm': 'гроза'
    }
    return weather_status_ru[weather_status_en]


def get_weather_celsius(data):
    celsius = round(data['main']['temp'] - 273.15)
    return celsius


def get_weather(user_city: str):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = open('WeatherApi/API key').read()
    city = user_city
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()
    return get_weather_status(response), get_weather_celsius(response)
