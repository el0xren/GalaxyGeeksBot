import aiohttp
from tg_bot import get_config
from tg_bot.core.logging import LOGE
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode

URL = "https://api.openweathermap.org/data/2.5/weather"

TEMP_UNITS = {"imperial": "F", "metric": "C"}

WIND_UNITS = {"imperial": "mph", "metric": "km/h"}


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        city = update.message.text.split(" ", 1)[1]
    except IndexError:
        await update.message.reply_text("City not provided")
        return

    if get_config("WEATHER_API_KEY", None) is None:
        await update.message.reply_text(
            "OpenWeatherMap API key not specified\n"
            "Ask the bot hoster to configure it")
        LOGE(
            "OpenWeatherMap API key not specified, get it at https://home.openweathermap.org/api_keys"
        )
        return

    parameters = {
        "appid": get_config("WEATHER_API_KEY", None),
        "q": city,
        "units": get_config("WEATHER_TEMP_UNIT", "metric"),
    }
    temp_unit = TEMP_UNITS.get(get_config("WEATHER_TEMP_UNIT", None), "K")
    wind_unit = WIND_UNITS.get(get_config("WEATHER_TEMP_UNIT", None), "km/h")

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=parameters) as response:
            data = await response.json()

            if data["cod"] != 200:
                await update.message.reply_text(f"Error: {data['message']}")
                return

            city_name = data["name"]
            city_country = data["sys"]["country"]
            city_lat = data["coord"]["lat"]
            city_lon = data["coord"]["lon"]
            weather_type = data["weather"][0]["main"]
            weather_type_description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            await update.message.reply_text(
                f"Current weather for {city_name}, {city_country} ({city_lat}, {city_lon}):\n"
                f"Weather: {weather_type} ({weather_type_description})\n"
                f"Temperature: {temp}{temp_unit} (Min: {temp_min}{temp_unit} Max: {temp_max}{temp_unit})\n"
                f"Humidity: {humidity}%\n"
                f"Wind: {wind_speed}{wind_unit}",
                parse_mode=ParseMode.MARKDOWN,
            )


# Define commands as CommandHandler instances
commands = [
    CommandHandler("weather", weather),
]
