import telebot 
import requests
from telebot import types
import logging

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = "8385966317:AAGbtrSpu9whxNzHhsZNVQHxxr1sq0eIuUQ"
elos = telebot.TeleBot(token)

# कॉन्फिगरेशन
API_URL = "http://fi8.bot-hosting.net:20163/elos-gpt3"
CHANNEL_URL = "https://t.me/REDX_64"
GROUP_URL = "https://t.me/+4qTbP-a9X7Q2Y2E9"
TIMEOUT = 10  # सेकंड

def create_main_markup():
    """मुख्य बटन मार्कअप बनाएं"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    channel_btn = types.InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🔗", url=CHANNEL_URL)
    group_btn = types.InlineKeyboardButton("𝗨𝗦𝗘 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣 👥", url=GROUP_URL)  # FIXED: Variable name
    markup.add(channel_btn, group_btn)
    return markup

def create_channel_markup():
    """सिर्फ चैनल बटन मार्कअप"""
    markup = types.InlineKeyboardMarkup()
    channel_btn = types.InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🔗", url=CHANNEL_URL)
    markup.add(channel_btn)
    return markup

# ग्रुप में /start command के लिए
@elos.message_handler(commands=['start'])
def start_message(message):
    try:
        if message.chat.type in ['group', 'supergroup']:
            welcome_text = """
𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧 𝗕𝗢𝗧! 🤖

⚡ 𝗡𝗢𝗪 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗚𝗥𝗢𝗨𝗣!

📌 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘:
`/redx your question`

📝 𝗘𝗫𝗔𝗠𝗣𝗟𝗘:
`/redx What is artificial intelligence?`

👉 𝗙𝗜𝗥𝗦𝗧 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟, 𝗧𝗛𝗘𝗡 𝗔𝗦𝗞 𝗤𝗨𝗘𝗦𝗧𝗜𝗢𝗡𝗦!
            """
            
            elos.send_message(message.chat.id, welcome_text, 
                             parse_mode='Markdown', 
                             reply_markup=create_main_markup())
        
        elif message.chat.type == 'private':
            private_welcome = """
🤖 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧 𝗕𝗢𝗧 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗! ⚡

✨ 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦:
• 𝗔𝗗𝗩𝗔𝗡𝗖𝗘𝗗 𝗔𝗜 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘𝗦
• 𝗚𝗥𝗢𝗨𝗣 & 𝗣𝗥𝗜𝗩𝗔𝗧𝗘 𝗦𝗨𝗣𝗣𝗢𝗥𝗧
• 𝗙𝗔𝗦𝗧 & 𝗔𝗖𝗖𝗨𝗥𝗔𝗧𝗘

📌 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣𝗦: Use `/redx your_question`
📌 𝗛𝗘𝗥𝗘: Just type your question

⚠️ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗙𝗜𝗥𝗦𝗧 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟!
            """
            
            elos.send_message(message.chat.id, private_welcome,
                             parse_mode='Markdown',
                             reply_markup=create_main_markup())
    
    except Exception as e:
        logger.error(f"Start error: {e}")
        elos.reply_to(message, "❌ Error in processing. Please try again.")

# ग्रुप में /redx command के लिए
@elos.message_handler(commands=['redx'])
def handle_redx(message):
    try:
        # चेक करें कि सवाल दिया गया है या नहीं
        if len(message.text.split()) < 2:
            markup = types.InlineKeyboardMarkup()
            channel_btn = types.InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🔗", url=CHANNEL_URL)
            example_btn = types.InlineKeyboardButton("𝗦𝗘𝗘 𝗘𝗫𝗔𝗠𝗣𝗟𝗘 📝", callback_data="show_example")
            markup.add(channel_btn)
            markup.add(example_btn)
            
            reply_msg = """
❌ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗔𝗦𝗞 𝗔 𝗤𝗨𝗘𝗦𝗧𝗜𝗢𝗡 𝗔𝗙𝗧𝗘𝗥 /redx

📌 𝗙𝗢𝗥𝗠𝗔𝗧: `/redx your question here`
📝 𝗘𝗫𝗔𝗠𝗣𝗟𝗘: `/redx What is AI?`

⚠️ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗙𝗜𝗥𝗦𝗧!
            """
            
            elos.reply_to(message, reply_msg, parse_mode='Markdown', reply_markup=markup)
            return
        
        # सवाल निकालें
        question = message.text.replace('/redx', '', 1).strip()
        
        if not question:
            elos.reply_to(message, 
                         "⚠️ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗧𝗬𝗣𝗘 𝗬𝗢𝗨𝗡𝗚 𝗤𝗨𝗘𝗦𝗧𝗜𝗢𝗡 𝗔𝗙𝗧𝗘𝗥 /redx 𝗖𝗢𝗠𝗠𝗔𝗡𝗗\n\n"
                         "𝗙𝗶𝗿𝘀𝘁 𝗷𝗼𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹: @REDX_64",
                         parse_mode='Markdown',
                         reply_markup=create_channel_markup())
            return
        
        # टाइपिंग इंडिकेटर भेजें
        elos.send_chat_action(message.chat.id, "typing")
        
        # AI API को कॉल करें
        response = requests.get(f"{API_URL}?text={question}", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "No response received.")
            
            # रिप्लाई भेजें
            reply_text = f"""
🔍 𝗤𝗨𝗘𝗦𝗧𝗜𝗢𝗡: {question}

🤖 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧:

{ai_response}

---
⚡ 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 𝗥𝗘𝗗𝗫𝟲𝟰 | [𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟]({CHANNEL_URL})
            """
            
            elos.reply_to(message, reply_text, parse_mode='Markdown')
            
        else:
            markup = types.InlineKeyboardMarkup()
            channel_btn = types.InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🔗", url=CHANNEL_URL)
            retry_btn = types.InlineKeyboardButton("𝗥𝗘𝗧𝗥𝗬 🔄", callback_data="retry_question")
            markup.add(channel_btn, retry_btn)
            
            elos.reply_to(message, 
                         "⚠️ 𝗔𝗜 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 𝗜𝗦 𝗖𝗨𝗥𝗥𝗘𝗡𝗧𝗟𝗬 𝗕𝗨𝗦𝗬.\n"
                         "𝗣𝗟𝗘𝗔𝗦𝗘 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡 𝗜𝗡 𝗔 𝗠𝗢𝗠𝗘𝗡𝗧.",
                         parse_mode='Markdown',
                         reply_markup=markup)
    
    except requests.exceptions.Timeout:
        elos.reply_to(message, 
                     "⏰ 𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗧𝗜𝗠𝗘𝗢𝗨𝗧. 𝗣𝗟𝗘𝗔𝗦𝗘 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡.\n\n"
                     "𝗝𝗼𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗳𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗲𝘀: @REDX_64",
                     parse_mode='Markdown',
                     reply_markup=create_channel_markup())
    except Exception as e:
        logger.error(f"Redx error: {e}")
        elos.reply_to(message, 
                     "❌ 𝗘𝗥𝗥𝗢𝗥 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗥𝗘𝗤𝗨𝗘𝗦𝗧.\n\n"
                     "𝗣𝗹𝗲𝗮𝘀𝗲 𝗷𝗼𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹: @REDX_64",
                     parse_mode='Markdown',
                     reply_markup=create_channel_markup())

# प्राइवेट चैट में सीधे सवाल के लिए
@elos.message_handler(func=lambda message: message.chat.type == 'private' and not message.text.startswith('/'))
def handle_private_question(message):
    try:
        question = message.text.strip()
        
        if not question:
            return
        
        # पहले चैनल ज्वाइन करने को बोलें
        elos.reply_to(message,
                     "⚠️ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗙𝗜𝗥𝗦𝗧 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟! 📢\n\n"
                     "𝗔𝗙𝗧𝗘𝗥 𝗝𝗢𝗜𝗡𝗜𝗡𝗚 𝗖𝗛𝗔𝗡𝗡𝗘𝗟, 𝗬𝗢𝗨 𝗖𝗔𝗡:\n\n"
                     "1️⃣ 𝗔𝗦𝗞 𝗤𝗨𝗘𝗦𝗧𝗜𝗢𝗡𝗦 𝗛𝗘𝗥𝗘 𝗗𝗜𝗥𝗘𝗖𝗧𝗟𝗬\n"
                     "2️⃣ 𝗨𝗦𝗘 `/redx` 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣𝗦\n\n"
                     "𝗖𝗛𝗔𝗡𝗡𝗘𝗟: @REDX_64",
                     parse_mode='Markdown',
                     reply_markup=create_main_markup())
        
        # फिर भी AI को सवाल भेजें
        elos.send_chat_action(message.chat.id, "typing")
        
        response = requests.get(f"{API_URL}?text={question}", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "No response received.")
            
            reply_text = f"""
🤖 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧:

{ai_response}

---
📌 𝗔𝗦𝗞 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣𝗦 𝗨𝗦𝗜𝗡𝗚: `/redx your_question`
🔗 [𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟]({CHANNEL_URL})
            """
            
            elos.send_message(message.chat.id, reply_text, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Private question error: {e}")

# कॉलबैक हैंडलर
@elos.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    try:
        if call.data == "show_example":
            example_text = """
📝 𝗖𝗢𝗥𝗥𝗘𝗖𝗧 𝗘𝗫𝗔𝗠𝗣𝗟𝗘𝗦:

1️⃣ `/redx What is artificial intelligence?`
2️⃣ `/redx Explain quantum computing`
3️⃣ `/redx How to learn Python?`
4️⃣ `/redx What are black holes?`

❌ 𝗪𝗥𝗢𝗡𝗚 𝗘𝗫𝗔𝗠𝗣𝗟𝗘𝗦:
• `/redx` (without question)
• Just `redx` (without slash)

⚠️ 𝗥𝗘𝗠𝗘𝗠𝗕𝗘𝗥: 𝗙𝗜𝗥𝗦𝗧 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟!
            """
            
            elos.answer_callback_query(call.id, "Example shown!")
            elos.send_message(call.message.chat.id, example_text, 
                             parse_mode='Markdown', 
                             reply_markup=create_channel_markup())
        
        elif call.data == "use_in_group":
            group_instructions = """
📢 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣:

1️⃣ 𝗔𝗗𝗗 𝗕𝗢𝗧 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣
2️⃣ 𝗦𝗘𝗡𝗗 `/start` 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣
3️⃣ 𝗨𝗦𝗘 `/redx your_question`

📌 𝗘𝗫𝗔𝗠𝗣𝗟𝗘:
`/redx What is machine learning?`

⚡ 𝗕𝗢𝗧 𝗪𝗜𝗟𝗟 𝗥𝗘𝗣𝗟𝗬 𝗜𝗡 𝗚𝗥𝗢𝗨𝗣!

⚠️ 𝗙𝗜𝗥𝗦𝗧 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟: @REDX_64
            """
            
            elos.answer_callback_query(call.id, "Group instructions sent!")
            elos.send_message(call.message.chat.id, group_instructions, 
                             parse_mode='Markdown', 
                             reply_markup=create_channel_markup())
        
        elif call.data == "retry_question":
            elos.answer_callback_query(call.id, "Please send your question again with /redx")
    
    except Exception as e:
        logger.error(f"Callback error: {e}")

if __name__ == "__main__":
    print("""
🤖 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧 𝗕𝗢𝗧 𝗜𝗦 𝗡𝗢𝗪 𝗪𝗢𝗥𝗞𝗜𝗡𝗚!
📢 𝗖𝗛𝗔𝗡𝗡𝗘𝗟: @REDX_64
⚡ 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 𝗥𝗘𝗗𝗫𝟲𝟰
✅ 𝗕𝗢𝗧 𝗜𝗦 𝗥𝗘𝗔𝗗𝗬 𝗧𝗢 𝗥𝗘𝗗-𝗫 𝗪𝗢𝗥𝗠 𝗚𝗣𝗧!
    """)
    
    try:
        elos.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
