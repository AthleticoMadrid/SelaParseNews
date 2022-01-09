import asyncio
import datetime
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from config import TOKEN as token_bot
from config import USER_ID as user_id
from main import check_news_update


bot = Bot(token=token_bot, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# функция клавиатуры:
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)                              #resize_keyboard - уменьшает размер кнопок клавиатуры
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


# функция сбора новостей:
@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                    f"{hlink(v['article_title'], v['article_url'])}"
                # f"{hunderline(v['article_title'])}\n" \
                # f"{hcode(v['article_desc'])}" 

        await message.answer(news)


# функция показывающая 5 последних новостей:
@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                    f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


# функция получения свежих новостей:
@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                        f"{hlink(v['article_title'], v['article_url'])}"
            await message.answer(news)
    
    else:
        await message.answer("Ещё нет свежих новостей.....")


# функция автоматически показывающая новые новости в боте:
async def news_every_minute():
    while True:
        fresh_news = check_news_update()
# если есть новая новость, то отправляем её:
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-5:]:
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                            f"{hlink(v['article_title'], v['article_url'])}"
# получить ID можно через @userinfobot (отправить ему /start)
                await bot.send_message(user_id, news, disable_notification=True)            #disable_notification - отправить сообщение в режиме без звука

        else:
            await bot.send_message(user_id, "Пока-что нет свежих новостей...")

        await asyncio.sleep(3600)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)