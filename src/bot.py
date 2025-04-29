import telebot
import os

# initialize bot

bot = telebot.TeleBot(
    os.environ['BOT_TOKEN'],
    parse_mode='HTML'
)