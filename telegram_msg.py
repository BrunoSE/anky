from telegram import Bot
import yaml
import asyncio
import time
from datetime import datetime
import pytz

newYorkTz = pytz.timezone("America/New_York") 

filename = "config.yaml"
try:
  with open(filename, "r") as file:
    config_data = yaml.safe_load(file)
except FileNotFoundError:
  raise FileNotFoundError(f"Error: YAML file not found: {filename}")

token = config_data["BOT_TOKEN"]
chat_id = config_data["CHANNEL_ID"]


def main():
    formatted_time = datetime.now(newYorkTz).strftime("%H:%M:%S")
    telegram_msg = f"Hello, the time is {formatted_time}"
    bot = Bot(token=token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=telegram_msg))
    print(telegram_msg)

if __name__ == "__main__":
    main()

