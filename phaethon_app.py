from flask import Flask, render_template, request, redirect, url_for
import datetime as dt
import requests
from flask import jsonify


app = Flask(__name__)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('api_key', 'r').read().strip()


# Функция для перевода температуры из кельвинов в цельсии
def kelvin_to_celsius(kelvin):
    return int(kelvin - 273.15)


@app.route('/', methods=["GET"])
def index():
    return render_template('home.html')


@app.route('/weather', methods=["POST"])
def get_weather():
    city = request.form['city-name']
    url = f"{BASE_URL}q={city}&appid={API_KEY}"
    response = requests.get(url).json()

    if response['cod'] == 200:
        temp_celsius = kelvin_to_celsius(response['main']['temp'])
        feels_like_celsius = kelvin_to_celsius(response['main']['feels_like'])
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        visibility = response['visibility']
        longitude = response['coord']['lon']
        latitude = response['coord']['lat']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']).strftime('%H:%M')
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']).strftime('%H:%M')
        city_name = response['name']
        country = response['sys']['country']
        
        return render_template('weather.html', 
                               city=city,
                               temp_celsius=temp_celsius,
                               feels_like_celsius=feels_like_celsius,
                               humidity=f"{humidity}%",
                               wind_speed=f"{wind_speed}m/s",
                               visibility=f"{visibility}m",
                               longitude=longitude,
                               latitude=latitude,
                               description=description,
                               sunrise_time=sunrise_time,
                               sunset_time=sunset_time,
                               city_name=city_name,
                               country=country)
    else:
        return redirect(url_for('error_page'))


@app.route('/error', methods=["GET"])
def error_page():
    return render_template('error.html')


@app.route('/registration', methods=["GET"])
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)