
import os
import telebot
import random
from telebot import types
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # ظ…ط«ظ„ https://your-app.onrender.com/

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ط§ظ„ط£ط³ط¦ظ„ط©
sections = {
    "ط§ط³ط¦ظ„ط© ط¯ظٹظ†ظٹط©": [
        {"q": "ظƒظ… ط¹ط¯ط¯ ط§ظ„طµظ„ظˆط§طھ ط§ظ„ظ…ظپط±ظˆط¶ط© ظپظٹ ط§ظ„ظٹظˆظ…طں", "options": ["3", "5", "7"], "answer": "5"},
        {"q": "ظ…ط§ ط§ط³ظ… ط£ظˆظ„ ط³ظˆط±ط© ظپظٹ ط§ظ„ظ‚ط±ط¢ظ†طں", "options": ["ط§ظ„ط¨ظ‚ط±ط©", "ط§ظ„ظپط§طھط­ط©", "ط§ظ„ظ†ط§ط³"], "answer": "ط§ظ„ظپط§طھط­ط©"},
        {"q": "ظƒظ… ط±ظƒط¹ط© ظپظٹ طµظ„ط§ط© ط§ظ„ظپط¬ط±طں", "options": ["2", "3", "4"], "answer": "2"},
        {"q": "ط£ظٹظ† ظ†ط²ظ„ ط§ظ„ظˆط­ظٹ ط¹ظ„ظ‰ ط§ظ„ظ†ط¨ظٹ ظ…ط­ظ…ط¯طں", "options": ["ط؛ط§ط± ط­ط±ط§ط،", "ظ…ظƒط©", "ط§ظ„ظ…ط¯ظٹظ†ط©"], "answer": "ط؛ط§ط± ط­ط±ط§ط،"},
        {"q": "ظ…ط§ ط§ط³ظ… ط§ظ„ظ†ط¨ظٹ ط§ظ„ط°ظٹ ط§ط¨طھظ„ط¹ظ‡ ط§ظ„ط­ظˆطھطں", "options": ["ظٹظˆظ†ط³", "ظٹظˆط³ظپ", "ظ…ظˆط³ظ‰"], "answer": "ظٹظˆظ†ط³"},
        {"q": "ظ…ط§ ط§ط³ظ… ط§ظ„طµظ„ط§ط© ط§ظ„طھظٹ طھطµظ„ظ‰ ط¹ظ†ط¯ ظƒط³ظˆظپ ط§ظ„ط´ظ…ط³طں", "options": ["ط§ظ„ط¶ط­ظ‰", "ط§ظ„ظƒط³ظˆظپ", "ط§ظ„ط§ط³طھط³ظ‚ط§ط،"], "answer": "ط§ظ„ظƒط³ظˆظپ"},
        {"q": "ظƒظ… ظ…ط±ط© ط°ظڈظƒط± ط§ط³ظ… ظ…ط­ظ…ط¯ ظپظٹ ط§ظ„ظ‚ط±ط¢ظ†طں", "options": ["3", "4", "5"], "answer": "4"},
        {"q": "ظ…ط§ ظ‡ظˆ ط¹ط¯ط¯ ط£ط´ظ‡ط± ط§ظ„ط­ط±ظ…طں", "options": ["2", "4", "6"], "answer": "4"},
        {"q": "ظ…ط§ ط§ط³ظ… ط¢ط®ط± ط³ظˆط±ط© ظپظٹ ط§ظ„ظ‚ط±ط¢ظ†طں", "options": ["ط§ظ„ظپظ„ظ‚", "ط§ظ„ط¥ط®ظ„ط§طµ", "ط§ظ„ظ†ط§ط³"], "answer": "ط§ظ„ظ†ط§ط³"},
        {"q": "ظ…ظ† ظ‡ظˆ ط®ط§طھظ… ط§ظ„ط£ظ†ط¨ظٹط§ط،طں", "options": ["ط¹ظٹط³ظ‰", "ظ…ظˆط³ظ‰", "ظ…ط­ظ…ط¯"], "answer": "ظ…ط­ظ…ط¯"},
    ],
    "ط£ظ„ط؛ط§ط²": [
        {"q": "ط´ظٹط، ط¥ط°ط§ ط£ظƒظ„طھظ‡ ظƒظ„ظ‡ طھط³طھظپظٹط¯طŒ ظˆط¥ط°ط§ ط£ظƒظ„طھ ظ†طµظ‡ طھظ…ظˆطھطں", "options": ["ط³ظ…ط³ظ…", "ط³ظ…ظƒ", "ط³ظ…"], "answer": "ط³ظ…"},
        {"q": "ظپظٹظ‡ ط¨ظٹطھ ظ…ط§ ظپظٹظ‡ ط£ط¨ظˆط§ط¨ ظˆظ„ط§ ظ†ظˆط§ظپط°طں", "options": ["ط¨ظٹطھ ط§ظ„ط´ط¹ط±", "ط¨ظٹطھ ط§ظ„ط¹ظ†ظƒط¨ظˆطھ", "ط¨ظٹطھ ط§ظ„ط±ط§ط­ط©"], "answer": "ط¨ظٹطھ ط§ظ„ط´ط¹ط±"},
        {"q": "ط´ظٹط، ظ…ط§ ظٹطھط¨ظ„ظ„ ظ„ظˆ ط­ط·ظٹطھظ‡ ط¨ط§ظ„ظ…ط§ط،طں", "options": ["ط§ظ„ط­ط¬ط±", "ط§ظ„ط³ظ…ظƒ", "ط§ظ„ط¸ظ„"], "answer": "ط§ظ„ط¸ظ„"},
        {"q": "ط£ظ…ظƒ ظˆط£ط®طھظƒطŒ ط¨ط³ ظ…ظˆ ط¨ظ†طھ ط£ظ…ظƒطں", "options": ["ط®ط§ظ„طھظƒ", "ط²ظˆط¬ط© ط£ط¨ظˆظƒ", "ط£ط®طھظƒ"], "answer": "ط®ط§ظ„طھظƒ"},
        {"q": "ظ…ط§ ظ‡ظˆ ط§ظ„ط´ظٹط، ط§ظ„ط°ظٹ ظٹظ…ط´ظٹ ظˆظٹظ‚ظپ ظˆظ„ظٹط³ ظ„ظ‡ ط£ط±ط¬ظ„طں", "options": ["ط§ظ„ط³ط§ط¹ط©", "ط§ظ„ظ‡ظˆط§ط،", "ط§ظ„ط¸ظ„"], "answer": "ط§ظ„ط³ط§ط¹ط©"},
        {"q": "ط´ظٹط، ظٹظƒطھط¨ ظˆظ„ط§ ظٹظ‚ط±ط£طں", "options": ["ط§ظ„ظ‚ظ„ظ…", "ط§ظ„ظƒطھط§ط¨", "ط§ظ„ظƒظ…ط¨ظٹظˆطھط±"], "answer": "ط§ظ„ظ‚ظ„ظ…"},
        {"q": "ظ…ط§ ظ‡ظˆ ط§ظ„ط´ظٹط، ط§ظ„ط°ظٹ ظٹظƒظˆظ† ط£ط®ط¶ط± ظپظٹ ط§ظ„ط£ط±ط¶ ظˆط£ط³ظˆط¯ ظپظٹ ط§ظ„ط³ظˆظ‚ ظˆط£ط­ظ…ط± ظپظٹ ط§ظ„ط¨ظٹطھطں", "options": ["ط§ظ„ظپظ„ظپظ„", "ط§ظ„ط´ط§ظٹ", "ط§ظ„ط²ظٹطھظˆظ†"], "answer": "ط§ظ„ط´ط§ظٹ"},
        {"q": "ظ„ظ‡ ط£ط³ظ†ط§ظ† ظˆظ„ط§ ظٹط¹ط¶طں", "options": ["ط§ظ„ظ…ط´ط·", "ط§ظ„ط³ظƒظٹظ†", "ط§ظ„ظ…ظ†ط´ط§ط±"], "answer": "ط§ظ„ظ…ط´ط·"},
        {"q": "ظƒظ„ظ…ط§ ط£ط®ط°طھ ظ…ظ†ظ‡ ظƒط¨ط±طں", "options": ["ط§ظ„ط­ظپط±ط©", "ط§ظ„ط¹ظ‚ظ„", "ط§ظ„ط®ط¨ط±ط©"], "answer": "ط§ظ„ط­ظپط±ط©"},
        {"q": "ظٹظ…ظ„ظƒ ط±ط£ط³ ظˆظ„ط§ ظٹظ…ظ„ظƒ ط¹ظٹظˆظ†طں", "options": ["ط§ظ„ط¥ط¨ط±ط©", "ط§ظ„ط¯ط¨ظˆط³", "ط§ظ„ط«ط¹ط¨ط§ظ†"], "answer": "ط§ظ„ط¥ط¨ط±ط©"},
    ],
    "ط§ط³ط¦ظ„ط© ط¹ط§ظ…ط©": [
        {"q": "ظ…ط§ ط¹ط§طµظ…ط© ط§ظ„ظٹط§ط¨ط§ظ†طں", "options": ["ط¨ظƒظٹظ†", "ط·ظˆظƒظٹظˆ", "ط³ظٹظˆظ„"], "answer": "ط·ظˆظƒظٹظˆ"},
        {"q": "ظ…ظ† ظ‡ظˆ ط£ظˆظ„ ط±ط¦ظٹط³ ظ„ظ„ظˆظ„ط§ظٹط§طھ ط§ظ„ظ…طھط­ط¯ط©طں", "options": ["ظ„ظٹظ†ظƒظˆظ„ظ†", "ط¬ظˆط±ط¬ ظˆط§ط´ظ†ط·ظ†", "ط£ظˆط¨ط§ظ…ط§"], "answer": "ط¬ظˆط±ط¬ ظˆط§ط´ظ†ط·ظ†"},
        {"q": "ظƒظ… ط¹ط¯ط¯ ظ‚ط§ط±ط§طھ ط§ظ„ط¹ط§ظ„ظ…طں", "options": ["5", "6", "7"], "answer": "7"},
        {"q": "ظ…ظ† ط§ط®طھط±ط¹ ط§ظ„ظ…طµط¨ط§ط­ ط§ظ„ظƒظ‡ط±ط¨ط§ط¦ظٹطں", "options": ["ط£ط¯ظٹط³ظˆظ†", "ط£ظٹظ†ط´طھط§ظٹظ†", "ظ†ظٹظˆطھظ†"], "answer": "ط£ط¯ظٹط³ظˆظ†"},
        {"q": "ظ…ط§ ظ‡ظˆ ط£ط¹ظ„ظ‰ ط¬ط¨ظ„ ظپظٹ ط§ظ„ط¹ط§ظ„ظ…طں", "options": ["ظƒظ„ظٹظ…ظ†ط¬ط§ط±ظˆ", "ط¥ظٹظپط±ط³طھ", "ط§ظ„ظ‡ظٹظ…ط§ظ„ط§ظٹط§"], "answer": "ط¥ظٹظپط±ط³طھ"},
        {"q": "ظ…ظ† ظ‡ظˆ ظ…ط¤ط³ط³ ط´ط±ظƒط© ظ…ط§ظٹظƒط±ظˆط³ظˆظپطھطں", "options": ["ط³طھظٹظپ ط¬ظˆط¨ط²", "ط¥ظٹظ„ظˆظ† ظ…ط§ط³ظƒ", "ط¨ظٹظ„ ط؛ظٹطھط³"], "answer": "ط¨ظٹظ„ ط؛ظٹطھط³"},
        {"q": "ظ…ط§ ظ‡ظٹ ط¹ط§طµظ…ط© ظ…طµط±طں", "options": ["ط§ظ„ظ‚ط§ظ‡ط±ط©", "ط§ظ„ط±ط¨ط§ط·", "ط¹ظ…ط§ظ†"], "answer": "ط§ظ„ظ‚ط§ظ‡ط±ط©"},
        {"q": "ظƒظ… ط¹ط¯ط¯ ط£ظ„ظˆط§ظ† ظ‚ظˆط³ ظ‚ط²ط­طں", "options": ["6", "7", "8"], "answer": "7"},
        {"q": "ط£ط·ظˆظ„ ظ†ظ‡ط± ظپظٹ ط§ظ„ط¹ط§ظ„ظ…طں", "options": ["ط§ظ„ط£ظ…ط§ط²ظˆظ†", "ط§ظ„ط¯ط§ظ†ظˆط¨", "ط§ظ„ظ†ظٹظ„"], "answer": "ط§ظ„ظ†ظٹظ„"},
        {"q": "ط£ظٹ ط¯ظˆظ„ط© طھظڈط¹ط±ظپ ط¨ط£ط±ط¶ ط§ظ„ظپط±ط§ط¹ظ†ط©طں", "options": ["ط³ظˆط±ظٹط§", "ظ…طµط±", "ط§ظ„ط¹ط±ط§ظ‚"], "answer": "ظ…طµط±"},
    ]
}

responses_correct = ["طµط­ ط¹ظ„ظٹظƒ ظٹط§ ظˆط­ط´ ًںکژ", "ط¨ط±ط§ظپظˆ ظˆط§ظ„ظ„ظ‡ ط§ظ†ظƒ ظپط§ظ‡ظ…ظ‡ط§ ًں‘ڈ", "ظ‡ظٹظƒ ط§ظ„ط´ط؛ظ„ ط§ظ„طµط­! ًںکŒ"]
responses_wrong = ["ط؛ظ„ط· ظٹط§ ط²ظ„ظ…ط© ًںŒڑ", "ظ…ط§ ط¶ط¨ط·طھ ظ…ط¹ظƒ ظ‡ط§ظٹ ًں’”", "ط­ط§ظˆظ„ ظ…ط±ط© طھط§ظ†ظٹط© ًںک‚"]
user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for section in sections.keys():
        markup.add(section)
    bot.send_message(message.chat.id, "ط§ط®طھط± ظ†ظˆط¹ ط§ظ„ط£ط³ط¦ظ„ط© ظٹظ„ظٹ ط¨ط¯ظƒ طھط¬ط±ط¨ ط­ط¸ظƒ ظپظٹظ‡ط§:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in sections.keys())
def handle_section(message):
    section = message.text
    questions = sections[section]
    quiz = random.sample(questions, 10)  # ظƒظ„ ظ…ط±ط© ط£ط³ط¦ظ„ط© ظ…ط®طھظ„ظپط©
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
            comment = f"ظپط®ظ…ظ…ظ…ظ…! ط¬ط¨طھ ط§ظ„ط¹ظ„ط§ظ…ط© ط§ظ„ظƒط§ظ…ظ„ط© {rating} ًں‘ڈًںکژ"
        elif score >= out_of * 0.7:
            comment = f"ظ†طھظٹط¬طھظƒ ظ…ظ†ظٹط­ط©: {rating}طŒ ط¨ط³ ط´ط¯ ط­ظٹظ„ظƒ ط´ظˆظٹ ًںکŒ"
        elif score >= out_of * 0.4:
            comment = f"ط¬ط±ط¨ ظ‚ط³ظ… طھط§ظ†ظٹ ظٹظ…ظƒظ† طھظƒظˆظ† ظپط§ظ„ط­ ظپظٹظ‡ ًںŒڑ (ظ†طھظٹط¬طھظƒ: {rating})"
        else:
            comment = f"ظˆط§ظ„ظ„ظ‡ طµط¹ط¨ط© ظٹط§ ظ…ط¹ظ„ظ…طŒ ط¬ط¨طھ {rating} ًں’”ًںک‚"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("ط±ط¬ظˆط¹ ظ„ظ„ظ‚ط§ط¦ظ…ط© ط§ظ„ط±ط¦ظٹط³ظٹط©")
        bot.send_message(chat_id, comment, reply_markup=markup)
        user_state.pop(chat_id)
        return

    question = state["questions"][state["current"]]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for option in question["options"]:
        markup.add(option)
    bot.send_message(chat_id, f"ط§ظ„ط³ط¤ط§ظ„ {state['current']+1}: {question['q']}", reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def handle_answer(message):
    chat_id = message.chat.id
    if message.text == "ط±ط¬ظˆط¹ ظ„ظ„ظ‚ط§ط¦ظ…ط© ط§ظ„ط±ط¦ظٹط³ظٹط©":
        send_welcome(message)
        return

    if chat_id not in user_state:
        bot.reply_to(message, "ط§ظƒطھط¨ /start ظˆط¨ظ„ظ‘ط´ ظ…ظ† ط¬ط¯ظٹط¯ ًںŒڑ")
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

# Webhook setup
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def index():
    return "ط§ظ„ط¨ظˆطھ ط´ط؛ط§ظ„ ًں”¥", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
