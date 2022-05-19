import telebot
# pyTelegramBotAPI	4.3.1
from telebot import types
import requests # Требуется для "Прислать собаку"
import bs4 # требуется для get_anekdot()

bot = telebot.TeleBot('5255331774:AAHCU3lY_SjoYPOepjMFpcLdfqK7Zz-Rk6o')  # Создаем экземпляр бота

# -----------------------------------------------------------------------

@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

# -----------------------------------------------------------------------
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)
# -----------------------------------------------------------------------

@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)

    # -----------------------------------------------------------------------

    @bot.message_handler(content_types=['photo'])
    def get_messages(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Это " + message.content_type)

        photo = message.photo
        bot.send_message(message.chat.id, photo)

        # -----------------------------------------------------------------------

        @bot.message_handler(content_types=['video'])
        def get_messages(message):
            chat_id = message.chat.id
            bot.send_message(chat_id, "Это " + message.content_type)

            video = message.video
            bot.send_message(message.chat.id, video)

# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------

@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Главное меню")
    btn2 = types.KeyboardButton("❓ Помощь")
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке ПаЙтон".format(
                         message.from_user), reply_markup=markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Главное меню" or ms_text == "👋 Главное меню" or ms_text == "Вернуться в главное меню":  # ..........
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Развлечения")
        btn2 = types.KeyboardButton("WEB-камера")
        btn3 = types.KeyboardButton("Управление")
        back = types.KeyboardButton("Помощь")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)

    elif ms_text == "Развлечения":  # ..................................................................................
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Прислать собаку")
        btn2 = types.KeyboardButton("Прислать анекдот")
        btn4 = types.KeyboardButton("Имена")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn4, back)
        bot.send_message(chat_id, text="Развлечения", reply_markup=markup)



    elif ms_text == "/dog" or ms_text == "Прислать собаку":  # .........................................................
        contents = requests.get('https://random.dog/woof.json').json()
        urlDOG = contents['url']
        bot.send_photo(chat_id, photo=urlDOG, caption="Вот тебе собачка!")

    elif ms_text == "Прислать анекдот":  # .............................................................................
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Имена":
        bot.send_message(chat_id, text=get_name())

    elif ms_text == "WEB-камера":
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "Управление":  # ...................................................................................
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "Помощь" or ms_text == "/help":  # .................................................................
        bot.send_message(chat_id, "Автор: Кривонос Маргарита")
        bot.send_message(chat_id, "Напишите автору: https://t.me/Mar_gosha_17")


    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Я тебя слышу!!! Ваше сообщение: " + ms_text)

# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    z = ''
    s = requests.get('https://nekdo.ru/random/')
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    result_find = soup.select('.text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]
#--------------------------
def get_name():
        array_name = []
        n = requests.get('https://777name.com/imya/')
        soup = bs4.BeautifulSoup(n.text, "html.parser")
        find_name = soup.select('.gen_ru')
        for result in find_name:
            array_name.append(result.getText().strip())
        if len(array_name) > 0:
            return array_name[0]

#--------------------------------------------------------
# def get_wind_direction(deg, advanced_result=False):
#     l = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
#     l_adv = ['Северный', 'Северо-Восточный', 'Восточный', 'Юго-Восточный', 'Южный', 'Юго-Западный', 'Западный', 'Северо-Западный']
#     for i in range(0, 8):
#         step = 45.
#         min = i * step - 45 / 2.
#         max = i * step + 45 / 2.
#         if i == 0 and deg > 360 - 45 / 2.:
#             deg = deg - 360
#         if deg >= min and deg <= max:
#             res = l_adv[i] if advanced_result else l[i]
#             break
#     return res
#
#
# def geohash(latitude, longitude, datedow):
#     '''Compute geohash() using the Munroe algorithm.
#     >>> geohash(37.421542, -122.085589, b'2005-05-26-10458.68')
#     37.857713 -122.544543
#     '''
#     # https://xkcd.com/426/
#     h = hashlib.md5(datedow, usedforsecurity=False).hexdigest()
#     p, q = [('%f' % float.fromhex('0.' + x)) for x in (h[:16], h[16:32])]
#     print('%d%s %d%s' % (latitude, p[1:], longitude, q[1:]))
#
#
# class OpenWeatherMap():
#     # для получения своего бесплатного ключа пройдите регистрацию: https://home.openweathermap.org/users/sign_up
#
#     def __init__(self):
#         pass
#-----------------------------------------------

# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0) # Запускаем бота

print()
# --------------------------

