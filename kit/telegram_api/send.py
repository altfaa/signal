from kit.names.channel import CHANNEL_NAME
from kit.tokens.telegram import telegram_token_A
from telebot import TeleBot


def send_photo_to_my_channel(photo_fp, text_message):
    try:
        bot = TeleBot(telegram_token_A)
        bot.send_photo(chat_id=CHANNEL_NAME, photo=photo_fp, caption=text_message, parse_mode='Markdown')
        bot.close()
    except Exception as e:
        print(e)
