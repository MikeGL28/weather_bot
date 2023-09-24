from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime
import requests
import asyncio

from aiogram.dispatcher.filters import Text

import auth_data as ad


bot = Bot(ad.token_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Москва', 'Санкт-Петербург', 'Пхукет', 'Аланья', 'Великие Луки', 'Новосокольники']
    keyboard.add(*buttons)
    await message.answer(f"Привет! В каком городе ты хочешь посмотреть погоду?", reply_markup=keyboard)

city = ['Москва', 'Санкт-Петербург', 'Пхукет', 'Аланья', 'Великие Луки', 'Новосокольники']


@dp.message_handler(Text(equals=city))
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F328"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={ad.token_api_weather}&units=metric"
        )
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри за окно, не пойму что там за погода."

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"] - data["sys"]["sunrise"])
        await message.reply(f"***{datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}С° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n"
              f"Ветер: {wind} м/с\nВосход солнца: {sunrise_time}\n"
              f"Заход солнца: {sunset_time}\nПродолжительность светового дня: {length_of_the_day}\n"
              f"***Хорошего дня***")
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == "__main__":
    executor.start_polling(dp)
