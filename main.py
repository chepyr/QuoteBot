import os
import random

import telebot
from PIL import Image, ImageDraw, ImageFont, ImageOps
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
                         "The message for the quote wasn't found.")
        return
    if original_message.text is None:
        bot.send_message(message.chat.id,
                         "There's no text for a quote in the message.")
        return

    send_quote_photo(original_message)


def get_user_photo(user_id):
    try:
        all_user_photos = bot.get_user_profile_photos(user_id)
        photo = all_user_photos.photos[0][0]
    except IndexError:
        return None
    return photo.file_id


def forwarded_message(message):
    return message.forward_from is not None


def send_quote_photo(message):
    # check if message was forwarded
    if forwarded_message(message):
        user = message.forward_from
    else:
        user = message.from_user

    user_first_name = user.first_name if user.first_name is not None else ''
    user_last_name = user.last_name if user.last_name is not None else ''
    text = message.text
    user_photo_id = get_user_photo(user.id)

    quote_photo_id = create_quote_photo(text,
                                        f"{user_first_name} {user_last_name}",
                                        user_photo_id)
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
    lines[0] = '«' + lines[0]
    lines[-1] = lines[-1] + ' ».'
    return lines


def create_image(lines):
    image_height = 600 if len(lines) < 4 else 400 + len(lines) * 58
    image_width = 1200
    image = Image.new('RGB', (image_width, image_height), color=(10, 10, 10))
    return image


def make_photo_rounded(path):
    size = (150, 150)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    im = Image.open(path)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    os.remove(path)
    return output


def draw_user_avatar(quote_image, user_photo_id):
    if user_photo_id is not None:
        file = bot.get_file(user_photo_id)
        user_avatar_bytes = bot.download_file(file.file_path)

        user_photo_path = f"{file.file_id}.jpg"
        with open(user_photo_path, 'wb') as file:
            file.write(user_avatar_bytes)

        round_user_photo = make_photo_rounded(user_photo_path)
        quote_image.paste(round_user_photo, (80, quote_image.height - 190), round_user_photo)


def create_quote_photo(text, username, user_photo_id):
    lines = split_text_into_rows(text)
    image = create_image(lines)

    draw = ImageDraw.Draw(image)
    draw.text((400, 100), text="Great People Quotes", fill=FONT_COLOR, font=FONT)
    draw.text((70, 200), text='\n'.join(lines), fill=FONT_COLOR, font=FONT)
    draw_user_avatar(image, user_photo_id)
    draw.text((260, image.height - 150), '© ' + username, fill=FONT_COLOR, font=FONT)

    # Saving
    photo_id = random.randint(1000000, 10000000)
    image.save(f'{photo_id}.jpg')
    return photo_id


if __name__ == '__main__':
    bot.polling(none_stop=True)
