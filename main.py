import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F
from aiogram.filters import Command
import secret

TOKEN = secret.API


session = AiohttpSession(proxy="http://proxy.server:3128")
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML),session=session)

@dp.message(Command("start"))
async def start(message: types.Message):

    await message.answer(
        "привет! отправь цитату и автора текстом, фоточку, видео или даже голосовое! но ни за что не присылай стикеры. мы предупредили.\n\nЧтобы узнать, какие команды есть в этом боте, напиши /cmds."
    )


@dp.message(Command("help"))
async def help(message: types.Message):

    await message.answer(
        "пример оформления цитаты:\n\nФункция забыла, что на ночь есть нельзя, и её разнесло\n© Кротов В.Г."
    )
    await message.answer("Держи значок копирайта:")
    await message.answer("©")


@dp.message(Command("cmds"))
async def cmds(message: types.Message):
    await message.answer(
        'нажми /help и получишь помощь по оформлению цитаты и значок копирайта\n\nнажми /rand и получишь случайную цитату из канала "квотес"\n\nнажми /stop и ты отпишешься от бота :('
    )


@dp.message(Command("stop"))
async def stop(message: types.Message):
    await message.answer(
        "ты больше не сможешь общаться с нами, "
        + message.chat.first_name
        + "( жаль, возвращайся к нам скорее\nесли ты хочешь снова отправить цитату, напиши /start"
    )


@dp.message(Command("rand"))
async def rand(message: types.Message):
    pass


@dp.message(F.content_type.in_({"voice"}))
async def voice(message: types.Message):

    if int(message.chat.id) != int(secret.ID):
        mes = (
            "<a href='tg://user?id="
            + str(message.chat.id)
            + "'>"
            + str(message.chat.first_name)
            + "</a> | <code>"
            + str(message.chat.id)
            + "</code>"
        )

        await bot.send_message(secret.ID, mes, parse_mode="html")
        to_pin = await bot.forward_message(
            secret.ID, message.chat.id, message.message_id
        )
        await bot.pin_chat_message(
            secret.ID, to_pin.message_id, disable_notification=True
        )

        await message.reply(
            f"{message.chat.first_name}, спасибо за... за что бы там ни было! 👍"
        )
    else:
        pass


@dp.message(F.content_type.in_({"photo"}))
async def photos(message):
    if int(message.chat.id) != int(secret.ID):
        mes = (
            "<a href='tg://user?id="
            + str(message.chat.id)
            + "'>"
            + str(message.chat.first_name)
            + "</a> | <code>"
            + str(message.chat.id)
            + "</code>"
        )
        await bot.send_message(secret.ID, mes, parse_mode="html")
        to_pin = await bot.forward_message(
            secret.ID, message.chat.id, message.message_id
        )
        await bot.pin_chat_message(
            secret.ID, to_pin.message_id, disable_notification=True
        )
        await bot.send_message(
            message.chat.id,
            "%s, спасибо за фоточку (надеюсь, на ней красоточка)! 👍"
            % message.chat.first_name,
        )
    else:
        pass


@dp.message(F.content_type.in_({"video"}))
async def videos(message):
    if int(message.chat.id) != int(secret.ID):
        mes = (
            "<a href='tg://user?id="
            + str(message.chat.id)
            + "'>"
            + str(message.chat.first_name)
            + "</a> | <code>"
            + str(message.chat.id)
            + "</code>"
        )
        await bot.send_message(secret.ID, mes, parse_mode="html")
        to_pin = await bot.forward_message(secret.ID, message.chat.id, message.message_id)
        await bot.pin_chat_message(
            secret.ID, to_pin.message_id, disable_notification=True
        )
        await bot.send_message(
            message.chat.id, "%s, спасибо за видосик! 👍" % message.chat.first_name
        )
    else:
        pass


@dp.message(F.content_type.in_({"sticker"}))
async def stickers(message):
    if int(message.chat.id) != int(secret.ID):
        await message.answer("%s, не спамь, а то получишь по жопе!" % message.chat.first_name)
    else:
        pass


@dp.message(F.content_type.in_({"text"}))
async def messages(message):
  if int(message.chat.id) == int(secret.ID):
    """
    try:
      chatId = message.text.split(': ')[0]
      text = message.text.split(': ')[1]
      if chatId == "@all":
        sql.execute('SELECT user_id FROM quot_users_bot')
        result = sql.fetchall()
        for x in result:
          bot.send_message(x[0], str(text))
      else:
        bot.send_message(chatId, text)
    except:
      pass
    """
    pass
  else:
    if message.chat.username is None:
      mes = "<a href='tg://user?id=" + str(message.chat.id) + "'>" + str(
        message.chat.first_name) + '</a> | <code>' + str(
          message.chat.id) + '</code>'
    else:
      mes = "<a href='https://t.me/" + str(message.chat.username) + "'>" + str(
        message.chat.first_name) + '</a> | <code>' + str(
          message.chat.id) + '</code>'

    to_pin = await bot.send_message(secret.ID,
                              mes + '\n\n<code>' + message.text + '</code>',
                              parse_mode='html')
    #bot.forward_message(config.owner, message.chat.id, message.id)
    #to_pin = bot.send_message(config.owner,'<code>' + message.text + '</code>', parse_mode='html')
    await bot.pin_chat_message(secret.ID,
                         to_pin.message_id,
                         disable_notification=True)
    await bot.send_message(message.chat.id,
                     '%s, спасибо за цитату! 👍' % message.chat.first_name)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls


    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
