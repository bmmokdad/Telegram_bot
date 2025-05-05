import os
import telebot
import random
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

sections = {
    "أسئلة دينية": [
        {"q": "كم عدد الصلوات المفروضة في اليوم؟", "a": ["5", "3", "4"], "c": "5"},
        {"q": "ما هي أول سورة في القرآن؟", "a": ["البقرة", "الفاتحة", "الناس"], "c": "الفاتحة"},
        {"q": "من هو خاتم الأنبياء؟", "a": ["محمد", "عيسى", "موسى"], "c": "محمد"},
        # ... زيد حتى 10
    ],
    "ألغاز": [
        {"q": "شي إذا أكلته كله تستفيد، وإذا أكلت نصه تموت؟", "a": ["سمسم", "سم", "سكر"], "c": "سم"},
        {"q": "ما هو الشيء الذي كلما أخذت منه يكبر؟", "a": ["الحفرة", "العقل", "العمر"], "c": "الحفرة"},
        {"q": "له رقبة وما إله رأس؟", "a": ["زجاجة", "إنسان", "ثعبان"], "c": "زجاجة"},
        # ... زيد حتى 10
    ],
    "أسئلة عامة": [
        {"q": "ما هي عاصمة اليابان؟", "a": ["طوكيو", "سول", "بكين"], "c": "طوكيو"},
        {"q": "من هو مكتشف أمريكا؟", "a": ["كريستوفر كولومبوس", "نيوتن", "أينشتاين"], "c": "كريستوفر كولومبوس"},
        {"q": "كم عدد قارات العالم؟", "a": ["6", "7", "5"], "c": "7"},
        # ... زيد حتى 10
    ],
    "جغرافيا": [
        {"q": "أين تقع الأهرامات؟", "a": ["مصر", "العراق", "السعودية"], "c": "مصر"},
        {"q": "ما هو أطول نهر في العالم؟", "a": ["الأمازون", "النيل", "الفرات"], "c": "النيل"},
        {"q": "أين تقع جبال الأنديز؟", "a": ["أمريكا الجنوبية", "أفريقيا", "آسيا"], "c": "أمريكا الجنوبية"},
        # ... زيد حتى 10
    ],
    "تاريخ": [
        {"q": "في أي سنة بدأت الحرب العالمية الأولى؟", "a": ["1914", "1939", "1900"], "c": "1914"},
        {"q": "من أول خليفة للمسلمين؟", "a": ["أبو بكر", "عمر", "عثمان"], "c": "أبو بكر"},
        {"q": "في أي دولة بدأت الثورة الفرنسية؟", "a": ["فرنسا", "ألمانيا", "إنجلترا"], "c": "فرنسا"},
        # ... زيد حتى 10
    ],
    "رياضة": [
        {"q": "كم لاعب في فريق كرة القدم؟", "a": ["11", "10", "12"], "c": "11"},
        {"q": "من فاز بكأس العالم 2018؟", "a": ["فرنسا", "الأرجنتين", "البرازيل"], "c": "فرنسا"},
        {"q": "كم عدد الأشواط في مباراة كرة السلة؟", "a": ["4", "2", "3"], "c": "4"},
        # ... زيد حتى 10
    ],
}

start_replies = [
    "هلا بالمثقف، جاهز؟",
    "يلا نبلّش يا ملك!",
    "جهّز حالك، جاييك تحدي 🔥"
]

right_replies = ["صح عليك يا فهيم 😎", "إجابة نارية! 🔥", "ما شاء الله عليك!", "هيك الشغل 😌", "مبدع والله!"]
wrong_replies = ["غلط يا معلم 🌚", "هاي ما زبطت معك 💔", "جرب غير خيار", "لسا بدك تدريب 😂"]

result_text = {
    0: "صفر؟! يا حرام جرب تلعب طاولة أحسن 🌚",
    1: "واحد من عشرة؟ يعني شوي وبتكسر الرقم القياسي بالعك 😂",
    5: "نص نص، حاول المرة الجاي تركّز",
    7: "والله قريب من الاحتراف، بس لسا في أمل",
    10: "عشرة من عشرة! مين بدو ينافسك؟! 👏👏👏"
}

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in sections.keys():
        markup.add(types.KeyboardButton(s))
    bot.send_message(message.chat.id, random.choice(start_replies), reply_markup=markup)
    users[message.chat.id] = {"section": None, "index": 0, "score": 0, "questions": []}

@bot.message_handler(func=lambda msg: msg.text in sections.keys())
def section_handler(message):
    section = message.text
    users[message.chat.id]["section"] = section
    users[message.chat.id]["index"] = 0
    users[message.chat.id]["score"] = 0
    users[message.chat.id]["questions"] = random.sample(sections[section], 10)
    send_question(message.chat.id)

def send_question(chat_id):
    user = users[chat_id]
    index = user["index"]
    if index >= len(user["questions"]):
        send_result(chat_id)
        return
    q = user["questions"][index]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for a in q["a"]:
        markup.add(types.KeyboardButton(a))
    bot.send_message(chat_id, f"السؤال {index+1}: {q['q']}", reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def answer_handler(message):
    user = users.get(message.chat.id)
    if not user or not user.get("section"):
        return

    index = user["index"]
    if index >= len(user["questions"]):
        return

    correct_answer = user["questions"][index]["c"]
    if message.text == correct_answer:
        user["score"] += 1
        reply = random.choice(right_replies)
    else:
        reply = random.choice(wrong_replies)

    bot.send_message(message.chat.id, reply)
    user["index"] += 1
    send_question(message.chat.id)

def send_result(chat_id):
    user = users[chat_id]
    score = user["score"]
    text = f"خلصنا! نتيجتك: {score}/10\n"
    comment = result_text.get(score, "يعني مش بطّال، بس في مجال تتحسّن 😅")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in sections.keys():
        markup.add(types.KeyboardButton(s))
    bot.send_message(chat_id, text + comment, reply_markup=markup)
    users[chat_id] = {"section": None, "index": 0, "score": 0, "questions": []}

print("البوت شغّال... استناه يجلط الناس بالأسئلة")
bot.polling()
