import telebot
import os

# initialize bot

bot = telebot.TeleBot(
    os.environ['BOT_TOKEN'],
    parse_mode='HTML'
)

gemini_api_key = os.environ['GEMINI_API_KEY']