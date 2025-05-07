import telebot
import random
import json
from flask import Flask, request

TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# تحميل الأسئلة من الملف
with open('questions_data.json', 'r', encoding='utf-8') as file:
    all_questions = json.load(file)

# دالة للحصول على 10 أسئلة عشوائية من قسم معيّن
def get_random_questions(section):
    return random.sample(all_questions[section], 10)

# تخزين حالة المستخدم
user_state = {}

# الرد على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("أسئلة دينية", "أسئلة عامة")
    markup.row("أسئلة جغرافيا", "أسئلة تاريخ")
    markup.row("ألغاز")
    bot.send_message(message.chat.id, "أهلين فيك! اختر نوع الأسئلة يلي بدك ياها:", reply_markup=markup)

# استقبال النوع المختار
@bot.message_handler(func=lambda message: message.text in all_questions.keys())
def handle_question_type(message):
    q_type = message.text
    user_state[message.chat.id] = {
        'type': q_type,
        'questions': get_random_questions(q_type),
        'index': 0,
        'score': 0
    }
    send_question(message.chat.id)

def send_question(chat_id):
    state = user_state.get(chat_id)
    if state and state['index'] < len(state['questions']):
        q_data = state['questions'][state['index']]
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in q_data['options']:
            markup.add(option)
        bot.send_message(chat_id, f"السؤال {state['index'] + 1}:\n{q_data['question']}", reply_markup=markup)
    else:
        finish_quiz(chat_id)

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def handle_answer(message):
    state = user_state[message.chat.id]
    q_data = state['questions'][state['index']]
    if message.text == q_data['answer']:
        state['score'] += 1
        bot.reply_to(message, random.choice(["صح عليك!", "جبتها!", "إجابة صحيحة!", "مبدع والله"]))
    else:
        bot.reply_to(message, f"غلط! الجواب الصحيح: {q_data['answer']}")
    state['index'] += 1
    send_question(message.chat.id)

def finish_quiz(chat_id):
    state = user_state.get(chat_id)
    score = state['score']
    if score == 10:
        msg = "مكسر الدنيا! 10/10!"
    elif score >= 7:
        msg = f"نتيجتك {score}/10، ممتاز!"
    elif score >= 4:
        msg = f"{score}/10، حاول مرّة تانية!"
    else:
        msg = f"{score}/10، فكر أكتر شوي المرة الجاي!"
    bot.send_message(chat_id, msg, reply_markup=telebot.types.ReplyKeyboardRemove())
    del user_state[chat_id]

# Flask Webhook
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/", methods=['GET'])
def index():
    return "البوت شغّال تمام", 200
