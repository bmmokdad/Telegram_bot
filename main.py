import os
import telebot
import random
from telebot import types
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # مثال: https://your-app.onrender.com

if not BOT_TOKEN or not WEBHOOK_URL:
    raise Exception("BOT_TOKEN أو WEBHOOK_URL مفقود من Environment Variables")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# الأسئلة (نفس اللي عندك بالضبط، ما تغيرت)
# --- [ضع هنا قسم الأسئلة كامل مثل اللي أرسلته فوق] ---

# الردود والتخزين
responses_correct = ["صح عليك يا وحش 😎", "برافو والله انك فاهمها 👏", "هيك الشغل الصح! 😌"]
responses_wrong = ["غلط يا زلمة 🌚", "ما ضبطت معك هاي 💔", "حاول مرة تانية 😂"]
user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for section in sections.keys():
        markup.add(section)
    bot.send_message(message.chat.id, "اختر نوع الأسئلة يلي بدك تجرب حظك فيها:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in sections.keys())
def handle_section(message):
    section = message.text
    questions = random.sample(sections[section], 10)
    user_state[message.chat.id] = {
        "section": section,
        "questions": questions,
        "score": 0,
        "current": 0
    }
    send_question(message.chat.id)

def send_question(chat_id):
    state = user_state.get(chat_id)
    if state["current"] >= len(state["questions"]):
        score = state["score"]
        out_of = len(state["questions"])
        rating = f"{score}/{out_of}"
        if score == out_of:
            comment = f"فخمممم! جبت العلامة الكاملة {rating} 👏😎"
        elif score >= out_of * 0.7:
            comment = f"نتيجتك منيحة: {rating}، بس شد حيلك شوي 😌"
        elif score >= out_of * 0.4:
            comment = f"جرب قسم تاني يمكن تكون فالح فيه 🌚 (نتيجتك: {rating})"
        else:
            comment = f"والله صعبة يا معلم، جبت {rating} 💔😂"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("رجوع للقائمة الرئيسية")
        bot.send_message(chat_id, comment, reply_markup=markup)
        user_state.pop(chat_id)
        return

    question = state["questions"][state["current"]]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for option in question["options"]:
        markup.add(option)
    bot.send_message(chat_id, f"السؤال {state['current']+1}: {question['q']}", reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def handle_answer(message):
    chat_id = message.chat.id
    if message.text == "رجوع للقائمة الرئيسية":
        send_welcome(message)
        return

    if chat_id not in user_state:
        bot.reply_to(message, "اكتب /start وبلّش من جديد 🌚")
        return

    state = user_state[chat_id]
    current_q = state["questions"][state["current"]]
    if message.text == current_q["answer"]:
        response = random.choice(responses_correct)
        state["score"] += 1
    else:
        response = random.choice(responses_wrong)

    bot.send_message(chat_id, response)
    state["current"] += 1
    send_question(chat_id)

# Webhook Routes
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def index():
    return "البوت شغال 🔥", 200

# تشغيل التطبيق مع تعيين الـ webhook
if __name__ == "__main__":
    full_webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{BOT_TOKEN}"
    success = bot.remove_webhook()
    print(f"Webhook removed: {success}")
    success = bot.set_webhook(url=full_webhook_url)
    print(f"Webhook set to: {full_webhook_url}, Success: {success}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
