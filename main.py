import telebot
from flask import Flask, request
import random
import json
import os

# إعدادات التوكن ورابط الويب هوك
TOKEN = "7646007283:AAGUiDAXOiHDW08gDuOTZHYLEciCwjlSnlA"
APP_URL = "https://telegram-bot-v3sv.onrender.com/" + TOKEN

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# تحميل الأسئلة من ملف
def load_questions(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# الأسئلة حسب القسم
question_files = {
    "general": "general_questions.json",
    "geo": "geo_questions.json"
}

# الرد على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("أسئلة عامة", "جغرافيا")
    bot.send_message(message.chat.id, "أهلا فيك! اختر نوع الأسئلة يلي بدك ياها:", reply_markup=markup)

# استقبال الرسائل واختيار نوع الأسئلة
@bot.message_handler(func=lambda message: message.text in ["أسئلة عامة", "جغرافيا"])
def handle_category(message):
    category = "general" if message.text == "أسئلة عامة" else "geo"
    questions = load_questions(question_files[category])
    question = random.choice(questions)
    bot.send_message(message.chat.id, f"سؤال:\n{question['question']}")
    bot.register_next_step_handler(message, check_answer, question['answer'])

# التحقق من الجواب
def check_answer(message, correct_answer):
    if message.text.strip().lower() == correct_answer.strip().lower():
        bot.send_message(message.chat.id, "صح عليك! ✅")
    else:
        bot.send_message(message.chat.id, f"غلط! ❌ الجواب الصحيح هو: {correct_answer}")

# إعدادات الويب هوك
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def index():
    return "البوت شغال تمام!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
