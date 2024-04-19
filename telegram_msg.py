from telegram import Bot
import yaml
import asyncio
import time
from datetime import datetime
import pytz

def days_since(year,month,day):
  today = date.today()
  special_date = date(year,month,day)

  # Calculate days passed
  days_passed = (today - special_date).days
  return days_passed

# Get the number of days passed
days_passed = days_since(2024, 3, 30)
print(f"Number of days passed: {days_passed}")
DAYS = 19

newYorkTz = pytz.timezone("America/New_York") 
filename = "config.yaml"

telegram_msg = ''
try:
  with open(f'chapters/chapter_{DAYS}.txt', "r") as file:
    telegram_msg = file.read()
except FileNotFoundError:
  raise FileNotFoundError(f"Error: file not found: chapter_{DAYS}.txt")


try:
  with open(filename, "r") as file:
    config_data = yaml.safe_load(file)
except FileNotFoundError:
  raise FileNotFoundError(f"Error: YAML file not found: {filename}")

token = config_data["BOT_TOKEN"]
chat_id = config_data["CHANNEL_ID"]


def main(telegram_msg):
    formatted_time = datetime.now(newYorkTz).strftime("%H:%M:%S")
    bot = Bot(token=token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=telegram_msg))
    print(telegram_msg)

if __name__ == "__main__":
    main(telegram_msg)

