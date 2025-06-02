import telebot
from telebot import types

BOT_TOKEN = '7766769017:AAG2ZwvXIwH2RjYdslQQZEsDjqQb1g5l3IQ'
bot = telebot.TeleBot(BOT_TOKEN)

# Удаляем Webhook, если он активен
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 Играть", "👥 Мои рефералы")
    bot.send_message(
        message.chat.id,
        "🎰 Добро пожаловать в казино-бота!\n\nВыберите действие:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🎲 Играть")
def handle_game(message):
    bot.send_dice(message.chat.id, emoji="🎲")

@bot.message_handler(func=lambda m: m.text == "👥 Мои рефералы")
def handle_referrals(message):
    bot.send_message(message.chat.id, "👥 Реферальная система будет доступна позже.")

print("🤖 Бот запущен...")
bot.polling()
