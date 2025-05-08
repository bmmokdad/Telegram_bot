# الرد على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("أسئلة دينية", "أسئلة عامة")
    markup.row("أسئلة جغرافيا", "أسئلة تاريخ")
    markup.row("ألغاز")
    bot.send_message(message.chat.id, "أهلين فيك! اختر نوع الأسئلة يلي بدك ياها:", reply_markup=markup)
import telebot
import random
import json
from flask import Flask, request

API_TOKEN = 'توكن_البوت_تبعك'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ملفات الأسئلة
QUESTION_FILES = {
    "أسئلة عامة": "general_questions.json",
    "جغرافيا": "geo_questions.json"
}

# الأسئلة المحمّلة
questions_data = {}

# تحميل الأسئلة من ملفات JSON
def load_questions():
    for category, file_name in QUESTION_FILES.items():
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                questions_data[category] = json.load(file)
        except Exception as e:
            print(f"خطأ بتحميل {file_name}: {e}")
            questions_data[category] = []

load_questions()

# حفظ بيانات المستخدمين مؤقتًا
user_data = {}

# إرسال قائمة الأقسام
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in QUESTION_FILES.keys():
        markup.add(category)
    bot.send_message(message.chat.id, "أهلين وسهلين! اختار نوع الأسئلة يلّي بدك ياها:", reply_markup=markup)

# لما يختار المستخدم نوع الأسئلة
@bot.message_handler(func=lambda message: message.text in QUESTION_FILES.keys())
def start_questions(message):
    category = message.text
    user_id = message.chat.id

    # نختار 10 أسئلة عشوائيًا
    selected_questions = random.sample(questions_data[category], min(10, len(questions_data[category])))

    user_data[user_id] = {
        "questions": selected_questions,
        "current_q": 0,
        "score": 0,
        "category": category
    }

    send_next_question(message.chat.id)

# إرسال السؤال التالي
def send_next_question(user_id):
    data = user_data.get(user_id)
    if data and data["current_q"] < len(data["questions"]):
        question_text = data["questions"][data["current_q"]]["question"]
        bot.send_message(user_id, f"سؤال {data['current_q'] + 1}: {question_text}")
    else:
        # خلصت الأسئلة
        score = data["score"]
        feedback = "عفيه عليك! نتيجتك ممتازة!" if score >= 8 else "تمام، بس بدها شوية مراجعة!" if score >= 5 else "يييي لازم تراجع دروسك!"
        bot.send_message(user_id, f"خلصنا! نتيجتك: {score} من {len(data['questions'])}\n{feedback}")
        del user_data[user_id]

# لما يجاوب المستخدم
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def check_answer(message):
    data = user_data[message.chat.id]
    correct_answer = data["questions"][data["current_q"]]["answer"].strip().lower()
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer:
        bot.send_message(message.chat.id, random.choice(["صح عليك يا وحش! 😎", "إجابة نارية! 🔥", "تمام التمام!"]))
        data["score"] += 1
    else:
        bot.send_message(message.chat.id, f"غلط! الجواب الصح هو: {data['questions'][data['current_q']]['answer']}")

    data["current_q"] += 1
    send_next_question(message.chat.id)

# إعداد Webhook
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_messages([telebot.types.Update.de_json(request.stream.read().decode("utf-8")).message])
    return 'ok', 200

@app.route('/')
def index():
    return 'بوت الأسئلة شغال!'

# ضبط الـ webhook
bot.remove_webhook()
bot.set_webhook(url='https://YOUR_DOMAIN_HERE/' + API_TOKEN)
