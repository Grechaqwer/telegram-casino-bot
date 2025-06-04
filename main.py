
import telebot
from telebot import types

BOT_TOKEN = '7457631853:AAH8gFID4T_rH4TMUeWHaCuwXMkuEsSErzU'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 Играть", "👥 Мои рефералы", "💸 Пополнить", "📊 Профиль")
    bot.send_message(message.chat.id, "Добро пожаловать в казино-бота!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎲 Играть")
def handle_game(message):
    bot.send_dice(message.chat.id, emoji="🎲")

@bot.message_handler(func=lambda m: m.text == "👥 Мои рефералы")
def handle_referrals(message):
    bot.send_message(message.chat.id, "Рефералы: пока не реализовано.")

@bot.message_handler(func=lambda m: m.text == "💸 Пополнить")
def handle_topup(message):
    bot.send_message(message.chat.id, "Пополнение: пока не реализовано.")

@bot.message_handler(func=lambda m: m.text == "📊 Профиль")
def handle_profile(message):
    bot.send_message(message.chat.id, "Профиль: пока не реализовано.")

bot.polling()
