import telebot
import bittensor as bt
from config import apikey

# res = requests.post('localhost:5000/api')


TOKEN = apikey
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['chat'])
def echo_all(message):
  print(message)

  user = message.from_user.username
  prompt = message.text
  ans = llm(prompt)
  print(ans)
  bot.reply_to(message, ans)

bot.infinity_polling()