import os
import telebot
import random
from telebot import types
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# الأسئلة
sections = {
    "اسئلة دينية": [
        {"q": "كم عدد الصلوات المفروضة في اليوم؟", "options": ["3", "5", "7"], "answer": "5"},
        {"q": "ما اسم أول سورة في القرآن؟", "options": ["البقرة", "الفاتحة", "الناس"], "answer": "الفاتحة"},
        {"q": "كم ركعة في صلاة الفجر؟", "options": ["2", "3", "4"], "answer": "2"},
        {"q": "أين نزل الوحي على النبي محمد؟", "options": ["غار حراء", "مكة", "المدينة"], "answer": "غار حراء"},
        {"q": "ما اسم النبي الذي ابتلعه الحوت؟", "options": ["يونس", "يوسف", "موسى"], "answer": "يونس"},
        {"q": "ما اسم الصلاة التي تصلى عند كسوف الشمس؟", "options": ["الضحى", "الكسوف", "الاستسقاء"], "answer": "الكسوف"},
        {"q": "كم مرة ذُكر اسم محمد في القرآن؟", "options": ["3", "4", "5"], "answer": "4"},
        {"q": "ما هو عدد أشهر الحرم؟", "options": ["2", "4", "6"], "answer": "4"},
        {"q": "ما اسم آخر سورة في القرآن؟", "options": ["الفلق", "الإخلاص", "الناس"], "answer": "الناس"},
        {"q": "من هو خاتم الأنبياء؟", "options": ["عيسى", "موسى", "محمد"], "answer": "محمد"},
    ],
    "ألغاز": [
        {"q": "شيء إذا أكلته كله تستفيد، وإذا أكلت نصه تموت؟", "options": ["سمسم", "سمك", "سم"], "answer": "سم"},
        {"q": "فيه بيت ما فيه أبواب ولا نوافذ؟", "options": ["بيت الشعر", "بيت العنكبوت", "بيت الراحة"], "answer": "بيت الشعر"},
        {"q": "شيء ما يتبلل لو حطيته بالماء؟", "options": ["الحجر", "السمك", "الظل"], "answer": "الظل"},
        {"q": "أمك وأختك، بس مو بنت أمك؟", "options": ["خالتك", "زوجة أبوك", "أختك"], "answer": "خالتك"},
        {"q": "ما هو الشيء الذي يمشي ويقف وليس له أرجل؟", "options": ["الساعة", "الهواء", "الظل"], "answer": "الساعة"},
        {"q": "شيء يكتب ولا يقرأ؟", "options": ["القلم", "الكتاب", "الكمبيوتر"], "answer": "القلم"},
        {"q": "ما هو الشيء الذي يكون أخضر في الأرض وأسود في السوق وأحمر في البيت؟", "options": ["الفلفل", "الشاي", "الزيتون"], "answer": "الشاي"},
        {"q": "له أسنان ولا يعض؟", "options": ["المشط", "السكين", "المنشار"], "answer": "المشط"},
        {"q": "كلما أخذت منه كبر؟", "options": ["الحفرة", "العقل", "الخبرة"], "answer": "الحفرة"},
        {"q": "يملك رأس ولا يملك عيون؟", "options": ["الإبرة", "الدبوس", "الثعبان"], "answer": "الإبرة"},
    ],
    "اسئلة عامة": [
        {"q": "ما عاصمة اليابان؟", "options": ["بكين", "طوكيو", "سيول"], "answer": "طوكيو"},
        {"q": "من هو أول رئيس للولايات المتحدة؟", "options": ["لينكولن", "جورج واشنطن", "أوباما"], "answer": "جورج واشنطن"},
        {"q": "كم عدد قارات العالم؟", "options": ["5", "6", "7"], "answer": "7"},
        {"q": "من اخترع المصباح الكهربائي؟", "options": ["أديسون", "أينشتاين", "نيوتن"], "answer": "أديسون"},
        {"q": "ما هو أعلى جبل في العالم؟", "options": ["كليمنجارو", "إيفرست", "الهيمالايا"], "answer": "إيفرست"},
        {"q": "من هو مؤسس شركة مايكروسوفت؟", "options": ["ستيف جوبز", "إيلون ماسك", "بيل غيتس"], "answer": "بيل غيتس"},
        {"q": "ما هي عاصمة مصر؟", "options": ["القاهرة", "الرباط", "عمان"], "answer": "القاهرة"},
        {"q": "كم عدد ألوان قوس قزح؟", "options": ["6", "7", "8"], "answer": "7"},
        {"q": "أطول نهر في العالم؟", "options": ["الأمازون", "الدانوب", "النيل"], "answer": "النيل"},
        {"q": "أي دولة تُعرف بأرض الفراعنة؟", "options": ["سوريا", "مصر", "العراق"], "answer": "مصر"},
    ]
}

responses_correct = ["صح عليك يا وحش 😎", "كفو الخاااال 👏", "هيك الشغل الصح! 😌"]
responses_wrong = ["غلط يا زلمة 🌚", "ما حبيتها منك يا خال 💔", "له يا خال 🌚 😂"]
user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for section in sections.keys():
        markup.add(section)
    bot.send_message(message.chat.id, "نقي نوع الأسئلة يلي بتحس حالك فالح فيها :", reply_markup=markup)

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
            comment = f" فخمممم! جبت العلامة الكاملة يا وحش {rating} 👏😎"
        elif score >= out_of * 0.7:
            comment = f"نتيجتك مليحة: {rating}، بس شد حيلك شوي 😌"
        elif score >= out_of * 0.4:
            comment = f"جرب قسم تاني يمكن تكون فالح فيه 🌚 (نتيجتك: {rating})"
        else:
            comment = f"والله صعبة يا خال، جبت {rating} 💔😂"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(" رجعني للقائمة الرئيسية يا خال 🌚")
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
    if message.text == "رجعني للقائمة الرئيسية ياخي":
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

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def index():
    return "البوت شغال 🔥", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
