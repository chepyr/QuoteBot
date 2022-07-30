import telebot
from private.config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=[''])
def start_message(message):
    bot.send_message(message.chat.id, 'Сообщение получено')


if __name__ == '__main__':
    bot.polling()
