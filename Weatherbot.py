import requests
import logging
from telegram import Bot
from dotenv import load_dotenv
import os
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, messagehandler


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
secret_token = os.getenv('TOKEN')

updater = Updater(token=secret_token)


API_KEY = os.getenv('API_KEY')
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
GEOCODER_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_PARAMS = {
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'ru'
}

GEOCODER_PARAMS = {
    'appid': API_KEY
}

def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Здравствуйте, {name}, я помогу узнать текущую погоду"""
    )
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Для того чтобы узнать погоду просто напишите название города."""
                             )

def get_city_coords(city):
    GEOCODER_PARAMS['q'] = city
    json = requests.get(GEOCODER_URL, GEOCODER_PARAMS).json()
    lat, lon = json[0]['lat'], json[0]['lon']
    return lat, lon


def get_weather(lat, lon):
    WEATHER_PARAMS['lat'], WEATHER_PARAMS['lon'] = lat, lon
    json = requests.get(WEATHER_URL, WEATHER_PARAMS).json()
    city = json['name']
    description = json['weather'][0]['description']
    temp = json['main']['temp']
    about = ''
    if temp <= 0:
        about='Одентесь потеплее!'
    elif 10>=temp>20 :
        about='Куртки будет достаточно)'
    elif temp>20:
        about = 'На улице достаточно тепло)'
    elif 'дождь' in description:
        about+='Возьмите зонтик)'

    return f'Погода в городе: {city}. {description.capitalize()}, температура: {temp} °C. {about}'


def return_weather(update, context):
    city = update['message']['text']
    chat = update.effective_chat
    crd = get_city_coords(city)
    weather = get_weather(crd[0], crd[1])
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""{weather}""")

def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, return_weather))
    updater.start_polling()

if __name__ == '__main__':
    main()