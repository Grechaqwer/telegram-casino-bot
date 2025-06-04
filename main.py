
import telebot
from telebot import types
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7766769017:AAG2ZwvXIwH2RjYdslQQZEsDjqQb1g5l3IQ")
bot = telebot.TeleBot(BOT_TOKEN)

users_file = "users.json"

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(users_file, "w") as f:
        json.dump(data, f)

users = load_users()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "referrals": [],
            "total_deposit": 0,
            "games_played": 0,
            "referrer": message.text.split()[1] if len(message.text.split()) > 1 else None
        }
        save_users(users)
        if users[user_id]["referrer"]:
            ref = users[user_id]["referrer"]
            if ref in users:
                users[ref]["referrals"].append(user_id)
                save_users(users)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 Играть", "👥 Мои рефералы")
    markup.add("💰 Пополнить", "💼 Профиль", "📈 Топ")
    bot.send_message(message.chat.id, "Добро пожаловать в казино-бота!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎲 Играть")
def handle_game(message):
    users[str(message.from_user.id)]["games_played"] += 1
    save_users(users)
    bot.send_dice(message.chat.id, emoji="🎲")

@bot.message_handler(func=lambda m: m.text == "👥 Мои рефералы")
def handle_referrals(message):
    u = users[str(message.from_user.id)]
    text = f"👥 Ваши рефералы: {len(u['referrals'])}\n"
    for rid in u['referrals']:
        text += f"— @{rid}\n"
    bot.send_message(message.chat.id, text or "У вас нет рефералов.")

@bot.message_handler(func=lambda m: m.text == "💰 Пополнить")
def handle_topup(message):
    link = "http://t.me/send?start=IVAsrLzRxoOB"
    bot.send_message(message.chat.id, f"Пополните баланс через кнопку ниже:\n{link}")

@bot.message_handler(func=lambda m: m.text == "💼 Профиль")
def profile(message):
    u = users[str(message.from_user.id)]
    ref_link = f"https://t.me/{bot.get_me().username}?start={message.from_user.id}"
    bot.send_message(message.chat.id, (
        "💼 Профиль:\n"
        f"💵 Баланс: {u['balance']}$\n"
        f"🎯 Игр сыграно: {u['games_played']}\n"
        f"📥 Пополнено: {u['total_deposit']}$\n"
        f"🔗 Ваша ссылка: {ref_link}"
    ))

@bot.message_handler(func=lambda m: m.text == "📈 Топ")
def top(message):
    top_text = "📈 Топ пополнений:\n"
    top_users = sorted(users.items(), key=lambda x: x[1]['total_deposit'], reverse=True)[:10]
    for i, (uid, data) in enumerate(top_users, 1):
        top_text += f"{i}. ID {uid}: {data['total_deposit']}$\n"
    bot.send_message(message.chat.id, top_text)

bot.polling()
