
import telebot
from telebot import types
import random

BOT_TOKEN = "7457631853:AAH8gFID4T_rH4TMUeWHaCuwXMkuEsSErzU"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

users = {}
referrals = {}
balances = {}
history = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    args = message.text.split()
    if user_id not in balances:
        balances[user_id] = 0
        history[user_id] = []
        if len(args) > 1:
            ref = args[1]
            if ref.isdigit() and int(ref) != user_id:
                referrals[user_id] = int(ref)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 Играть", "👥 Мои рефералы", "💰 Баланс")
    bot.send_message(message.chat.id, f"Добро пожаловать в Assassin Casino!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎲 Играть")
def play_game(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Чёт", callback_data="even"),
               types.InlineKeyboardButton("Нечёт", callback_data="odd"))
    bot.send_message(message.chat.id, "Выберите ставку:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["even", "odd"])
def handle_guess(call):
    user_id = call.from_user.id
    dice = random.randint(1, 6)
    win = (call.data == "even" and dice % 2 == 0) or (call.data == "odd" and dice % 2 == 1)
    result = "✅ Победа!" if win else "❌ Поражение!"
    amount = 1.00  # фиксированная ставка
    if win:
        balances[user_id] += amount
    else:
        balances[user_id] -= amount
        ref_id = referrals.get(user_id)
        if ref_id:
            balances[ref_id] += 0.25  # 25% с проигрыша
    history[user_id].append((call.data, dice, win))
    bot.send_message(call.message.chat.id, f"🎲 Выпало: {игральные кости}")
"💵" Баланс: {balances[user_id]:.2f}$")

@bot.message_handler(func=lambda m: m.text == "👥 Мои рефералы")
def referrals_handler(message):
    user_id = message.from_user.id
    invited = [uid for uid, ref in referrals.items() if ref == user_id]
    ref_count = len(invited)
    msg = f"👥 Ваши рефералы: {ref_count}

"
    for i, rid in enumerate(invited, 1):
        total_games = len(history.get(rid, []))
        msg += f"{i}. ID {rid}, игр: {total_games}
"
    msg += "
"🎁" За 25/50/100 рефералов вручную выдается: 2$/4.5$/10$.
Попросите выплату у администрации."
    msg += f"

"🔗" Ваша ссылка: https://t.me/assassincasino_bot?start={user_id}"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def balance_handler(message):
    user_id = message.from_user.id
    balance = balances.get(user_id, 0)
    bot.send_message(message.chat.id, f"💰 Ваш баланс: {balance:.2f}$")

bot.infinity_polling()
