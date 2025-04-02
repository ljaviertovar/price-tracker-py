import os
import telebot

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


def send_message(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)
