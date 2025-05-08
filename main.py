import telebot
import json
import random
from flask import Flask, request

API_TOKEN = '7646007283:AAGUiDAXOiHDW08gDuOTZHYLEciCwjlSnlA'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# خريطة الأزرار مع أسماء الملفات
question_files = {
    'أسئلة عامة': 'general_questions.json',
    'جغرافيا': 'geo_questions.json'
}

# دالة تحميل الأسئلة من ملف
def load_questions(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

# بداية المحادثة
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in question_files:
        markup.row(name)
    bot.send_message(message.chat.id, "اختار نوع الأسئلة:", reply_markup=markup)

# استقبال اختيار المستخدم
@bot.message_handler(func=lambda message: message.text in question_files)
def handle_question_category(message):
    filename = question_files[message.text]
    questions = load_questions(filename)
    
    if not questions:
        bot.send_message(message.chat.id, "صار في مشكلة بتحميل الأسئلة.")
        return

    # نختار سؤال عشوائي
    question = random.choice(questions)
    bot.send_message(message.chat.id, f"السؤال:\n{question['question']}")
    
    # ننتظر الجواب
    bot.register_next_step_handler(message, lambda msg: check_answer(msg, question['answer']))

# دالة التحقق من الجواب
def check_answer(message, correct_answer):
    if message.text.strip().lower() == correct_answer.strip().lower():
        bot.send_message(message.chat.id, "صح عليك! 😎")
    else:
        bot.send_message(message.chat.id, f"لأ غلط! الجواب الصحيح هو: {correct_answer}")

# إعداد الويب هوك لـ Render
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return 'ok', 200
    else:
        return 'Hello from Telegram bot', 200

# تعيين الويب هوك
bot.remove_webhook()
bot.set_webhook(url='https://telegram-bot-v3sv.onrender.com/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
