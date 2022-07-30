import telebot
from private.config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=[''])
def start_message(message):
    original_message = message.reply_to_message
    if original_message is None:
        bot.send_message(message.chat.id, 'Сообщение для цитаты не найдено')
        return

    user = original_message.from_user
    user_first_name = user.first_name if user.first_name is not None else ''
    user_last_name = user.last_name if user.last_name is not None else ''
    bot.send_message(message.chat.id,
                     f'Сообщение получено от {user_first_name} {user_last_name}')


if __name__ == '__main__':
    bot.polling()
