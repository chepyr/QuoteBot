import os
import random

import telebot
from PIL import Image, ImageDraw, ImageFont
from private.config import TOKEN

bot = telebot.TeleBot(TOKEN)
FONT = ImageFont.truetype("Chevin-Cyrillic-Bold_10486.ttf",
                          36, encoding='utf-8')


@bot.message_handler(commands=['', 'make_quote'])
def get_make_quote_command(message):
    original_message = message.reply_to_message
    if original_message is None:
        bot.send_message(message.chat.id, 'Сообщение для цитаты не найдено')
        return

    send_quote_photo(original_message)


def send_quote_photo(message):
    user = message.from_user
    user_first_name = user.first_name if user.first_name is not None else ''
    user_last_name = user.last_name if user.last_name is not None else ''
    text = message.text

    photo_id = create_quote_photo(text,
                                  f"{user_first_name} {user_last_name}",
                                  None)
    with open(f'{photo_id}.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove(f'{photo_id}.jpg')


def split_text_into_rows(text):
    return


def create_quote_photo(text, username, user_photo):
    image = Image.new('RGB', (1000, 600), color=(10, 10, 10))
    draw = ImageDraw.Draw(image)
    draw.text((30, 30), text=text, fill=(220, 220, 200), font=FONT)

    # Saving
    photo_id = random.randint(1000000, 10000000)
    image.save(f'{photo_id}.jpg')
    return photo_id


if __name__ == '__main__':
    bot.polling()
