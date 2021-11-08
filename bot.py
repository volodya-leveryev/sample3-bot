""" Telegrom Bot sample """

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BASE_URL = 'https://news.ykt.ru'


def start_cmd(update: Update, _context: CallbackContext):
    """ Start command """
    update.message.reply_text('Welcome!')


def get_news_cmd(update: Update, _context: CallbackContext):
    """ Getting news from site """
    html = requests.get(BASE_URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    wrapper = soup.find(id='left-float-wrapper')
    msg = 'Oops'
    link = wrapper.find_all('a', class_='n-latest-news_title_link')
    if link:
        link = link[0]
        url = BASE_URL + link['href']
        msg = f'<a href="{url}">{link.text}</a>'
    update.message.reply_html(msg)


def main():
    """ Main function """
    with open('token.txt', encoding='ascii') as token_file:
        token = token_file.readline()

    updater = Updater(token)

    # конфигурируем команды
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_cmd))
    dispatcher.add_handler(CommandHandler("get_news", get_news_cmd))

    updater.start_polling()  # запускаем бота
    updater.idle()  # ждем новых сообщений

if __name__ == '__main__':
    main()
