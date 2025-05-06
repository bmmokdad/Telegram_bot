import os
import telebot
import random
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# الأسئلة لكل قسم
sections = {
    "اسئلة دينية": [
        {"q": "كم عدد الصلوات المفروضة؟", "options": ["3", "5", "7"], "answer": "5"},
        {"q": "ما اسم أول سورة في القرآن؟", "options": ["البقرة", "الفاتحة", "الناس"], "answer": "الفاتحة"},
        {"q": "كم ركعة في صلاة الفجر؟", "options": ["2", "3", "4"], "answer": "2"},
        {"q": "أين نزل الوحي على النبي؟", "options": ["غار حراء", "مكة", "المدينة"], "answer": "غار حراء"},
        {"q": "ما اسم النبي الذي ابتلعه الحوت؟", "options": ["يونس", "يوسف", "موسى"], "answer": "يونس"},
    ],
    "ألغاز": [
        {"q": "شيء إذا أكلته كله تستفيد، وإذا أكلت نصه تموت؟", "options": ["سمسم", "سمك", "سم"], "answer": "سم"},
        {"q": "فيه بيت ما فيه أبواب ولا نوافذ؟", "options": ["بيت الشعر", "بيت العنكبوت", "بيت الراحة"], "answer": "بيت الشعر"},
        {"q": "شيء ما يتبلل لو حطيته بالماء؟", "options": ["الحجر", "السمك", "الظل"], "answer": "الظل"},
        {"q": "أمك وأختك، بس مو بنت أمك؟", "options": ["خالتك", "زوجة أبوك", "أختك"], "answer": "خالتك"},
    ],
    "اسئلة عامة": [
        {"q": "ما عاصمة اليابان؟", "options": ["بكين", "طوكيو", "سيول"], "answer": "طوكيو"},
        {"q": "من هو أول رئيس للولايات المتحدة؟", "options": ["لينكولن", "جورج واشنطن", "أوباما"], "answer": "جورج واشنطن"},
        {"q": "كم عدد قارات العالم؟", "options": ["5", "6", "7"], "answer": "7"},
        {"q": "من اخترع المصباح الكهربائي؟", "options": ["أديسون", "أينشتاين", "نيوتن"], "answer": "أديسون"},
    ]
}

responses_correct = ["صح عليك يا وحش 😎", "برافو والله انك فاهمها 👏", "هيك الشغل الصح! 😌"]
responses_wrong = ["غلط يا زلمة 🌚", "ما ضبطت معك هاي 💔", "حاول مرة تانية 😂"]

user_state = {}

# القائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for section in sections.keys():
        markup.add(section)
    bot.send_message(message.chat.id, "اختر نوع الأسئلة يلي بدك تجرب حظك فيها:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in sections.keys())
def handle_section(message):
    section = message.text
    questions = sections[section]
    sample_size = min(5, len(questions))  # نحط حد أقصى 5
    quiz = random.sample(questions, sample_size)
    user_state[message.chat.id] = {
        "section": section,
        "questions": quiz,
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

print("البوت شغال... استناه يستقبل رسائل.")
bot.polling()
