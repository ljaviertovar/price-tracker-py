from dotenv import load_dotenv
import os
import telebot

load_dotenv()

TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


def send_message(message):
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        print("Message sent successfully.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error to send message: {e}")
