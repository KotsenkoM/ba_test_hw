import logging
import os
import requests
import time

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

load_dotenv()
token = os.getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    '''Отправка стартового сообщения пользователю при запуске бота'''
    await message.reply(
        'Привет! Отправь мне ссылку, я сделаю скриншот и сохраню код ответа страницы.'
    )


@dp.message_handler(content_types=['text'])
async def take_screenshot(message):
    '''Создание скриншота страницы по ссылке, отправленной пользователем боту.
    Полученный скриншот и код страницы отправляется обратно пользователю.'''
    url = message.text
    ss = urlparse(url).netloc
    timestamp = time.strftime('%Y-%m-%d_%H:%M')
    ss_name = f'{timestamp}_<{ss}>.jpg'
    try:
        response = requests.get(url)
        driver = webdriver.Chrome()
        driver.get(url)
        el = driver.find_element(By.TAG_NAME, 'body')
        el.screenshot(ss_name)
        driver.quit()
        with open(ss_name, 'rb') as new_ss:
            await bot.send_photo(message.chat.id, new_ss)
            await bot.send_message(
                message.chat.id,
                f'Код ответа страницы: {response.status_code}'
            )
    except:
        await bot.send_message(
            message.chat.id,
            'Не удалось открыть ссылку! Пожалуйста, проверьте ссылку и попробуйте снова)'
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
