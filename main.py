import os
import random

import telebot
from PIL import Image, ImageDraw, ImageFont
from private.config import TOKEN

bot = telebot.TeleBot(TOKEN)
FONT = ImageFont.truetype("Chevin-Cyrillic-Light_10488.ttf",
                          50, encoding='utf-8')
FONT_COLOR = (240, 240, 230)


@bot.message_handler(commands=['', 'make_quote'])
def get_make_quote_command(message):
    original_message = message.reply_to_message
    if original_message is None:
        bot.send_message(message.chat.id,
                         "The message for the quote wasn't found")
        return

    send_quote_photo(original_message)


def get_user_photo(user_id):
    all_user_photos = bot.get_user_profile_photos(user_id)
    photo = all_user_photos.photos[0][0]
    return photo.file_id


def send_quote_photo(message):
    user = message.from_user
    user_first_name = user.first_name if user.first_name is not None else ''
    user_last_name = user.last_name if user.last_name is not None else ''
    text = message.text

    # getting user photo id
    user_photo_id = get_user_photo(message.from_user.id)
    bot.send_photo(message.chat.id, user_photo_id)

    quote_photo_id = create_quote_photo(text,
                                        f"{user_first_name} {user_last_name}",
                                        None)
    with open(f'{quote_photo_id}.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove(f'{quote_photo_id}.jpg')


def split_text_into_rows(text):
    lines = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        line = ''
        for word in words:
            if len(line + ' ' + word) > 50:
                lines.append(line)
                line = word
            else:
                line += ' ' + word
        lines.append(line)
    return lines


def create_quote_photo(text, username, user_photo):
    lines = split_text_into_rows(text)
    image_height = 600 if len(lines) < 4 else 350 + len(lines) * 57
    image_width = 1200

    # creating an image
    image = Image.new('RGB', (image_width, image_height), color=(10, 10, 10))
    draw = ImageDraw.Draw(image)
    # drawing a text
    draw.text((400, 100), text="Great People Quotes", fill=FONT_COLOR,
              font=FONT)
    draw.text((40, 200), text='\n'.join(lines), fill=FONT_COLOR, font=FONT)

    draw.text((100, image_height - 150), username, fill=FONT_COLOR, font=FONT)

    # Saving
    photo_id = random.randint(1000000, 10000000)
    image.save(f'{photo_id}.jpg')
    return photo_id


if __name__ == '__main__':
    bot.polling()
