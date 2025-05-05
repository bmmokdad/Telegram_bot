import os
import telebot
import random
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ردود متنوعة للصح والخطأ
correct_responses = ["صح عليك يا وحش 😎", "مبدع والله 👏", "هيك الشغل ولا بلاش 😌", "أيوه هيك نبيك! 😀"]
wrong_responses = ["يخرب بيت الذكاء 🌚", "غلط يا معلم 😂", "ضربت جنب 💔", "مو هووون الجواب 😅"]

# البيانات
questions = {
    "ألغاز": [
        {"q": "شيء يمشي بدون أرجل؟", "a": "الساعة", "choices": ["السيارة", "الساعة", "الهواء"]},
        {"q": "شيء إذا لمسته صرخ؟", "a": "الجرس", "choices": ["القط", "الجرس", "الهاتف"]},
        {"q": "شي بيجي بالليل وما يجي بالنهار؟", "a": "الظلام", "choices": ["القمر", "الظلام", "المنبه"]}
    ],
    "دينية": [
        {"q": "كم عدد أركان الإسلام؟", "a": "5", "choices": ["5", "4", "6"]},
        {"q": "ما أول سورة بالقرآن؟", "a": "الفاتحة", "choices": ["النساء", "البقرة", "الفاتحة"]},
        {"q": "ما اسم نبي ابتلعه الحوت؟", "a": "يونس", "choices": ["موسى", "نوح", "يونس"]}
    ],
    "جغرافيا": [
        {"q": "عاصمة اليابان؟", "a": "طوكيو", "choices": ["طوكيو", "بكين", "سول"]},
        {"q": "أطول نهر بالعالم؟", "a": "النيل", "choices": ["الأمازون", "الدانوب", "النيل"]},
        {"q": "أين تقع جبال الأنديز؟", "a": "أمريكا الجنوبية", "choices": ["آسيا", "أوروبا", "أمريكا الجنوبية"]}
    ],
    "تاريخ": [
        {"q": "من حرر القدس؟", "a": "صلاح الدين", "choices": ["صلاح الدين", "هولاكو", "نابليون"]},
        {"q": "كم سنة استمرت الحرب العالمية الثانية؟", "a": "6", "choices": ["4", "6", "10"]},
        {"q": "في أي عام سقطت بغداد على يد المغول؟", "a": "1258", "choices": ["1517", "1258", "1917"]}
    ],
    "رياضة": [
        {"q": "كم لاعب في فريق كرة القدم؟", "a": "11", "choices": ["9", "11", "10"]},
        {"q": "من فاز بكأس العالم 2018؟", "a": "فرنسا", "choices": ["فرنسا", "الأرجنتين", "ألمانيا"]},
        {"q": "عدد أشواط كرة السلة؟", "a": "4", "choices": ["2", "4", "3"]}
    ]
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("أسئلة دينية", "ألغاز", "أسئلة عامة")
    bot.send_message(message.chat.id, "اختار نوع الأسئلة يلي بدك تجرب حظك فيها:", reply_markup=markup)
    user_data[message.chat.id] = {"score": 0, "q_index": 0, "category": None}

@bot.message_handler(func=lambda m: m.text in ["أسئلة دينية", "ألغاز", "أسئلة عامة"])
def choose_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "أسئلة عامة":
        markup.add("جغرافيا", "تاريخ", "رياضة", "رجوع للقائمة")
        bot.send_message(message.chat.id, "اختار نوع الأسئلة العامة:", reply_markup=markup)
    else:
        user_data[message.chat.id] = {"score": 0, "q_index": 0, "category": message.text}
        send_question(message.chat.id)

@bot.message_handler(func=lambda m: m.text in ["جغرافيا", "تاريخ", "رياضة"])
def general_sub_category(message):
    user_data[message.chat.id] = {"score": 0, "q_index": 0, "category": message.text}
    send_question(message.chat.id)

def send_question(chat_id):
    data = user_data[chat_id]
    cat = data["category"]
    index = data["q_index"]
    if index < len(questions[cat]):
        q = questions[cat][index]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for choice in q["choices"]:
            markup.add(choice)
        bot.send_message(chat_id, f"سؤال {index + 1}: {q['q']}", reply_markup=markup)
    else:
        score = data["score"]
        msg = f"نتيجتك: {score} من 3\n"
        if score == 0:
            msg += "فشل ذريع 🌚 جرب شي أسهل"
        elif score == 1:
            msg += "أهااا، بتحاول يعني 😂"
        elif score == 2:
            msg += "قريب من الممتاز 😌"
        else:
            msg += "أسطورة زمانك يا غالي 😎"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("رجوع للقائمة")
        bot.send_message(chat_id, msg, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "رجوع للقائمة")
def back_to_menu(message):
    start(message)

@bot.message_handler(func=lambda m: True)
def answer_question(message):
    if message.chat.id not in user_data or not user_data[message.chat.id]["category"]:
        bot.send_message(message.chat.id, "بلّش أول شي من القائمة الرئيسية واختار نوع الأسئلة.")
        return
    data = user_data[message.chat.id]
    cat = data["category"]
    index = data["q_index"]
    if index < len(questions[cat]):
        correct = questions[cat][index]["a"]
        if message.text == correct:
            data["score"] += 1
            bot.send_message(message.chat.id, random.choice(correct_responses))
        else:
            bot.send_message(message.chat.id, random.choice(wrong_responses))
        data["q_index"] += 1
        send_question(message.chat.id)

print("البوت شغّال... استناه يشتغل")
bot.polling()
