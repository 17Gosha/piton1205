import telebot
import word.json

bot = telebot.TeleBot('5255331774:AAHCU3lY_SjoYPOepjMFpcLdfqK7Zz-Rk6o')

@bot.message_handler(commands=['start'])
def start_menu(message):
    button_list = ['gorod', 'zhivotnye', 'mebel', 'pogoda', 'posuda']
    bot.send_message(message.from_user.id, "выбери категорию", reply_markup= generate_menu_inline(button_list))
    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def get_word(call):
    if call.data == 'Вернуться в главное меню':
        button_list = ['gorod', 'zhivotnye', 'mebel', 'pogoda', 'posuda']
        bot.send_message(call.message.chat.id, "выбери категорию", reply_markup=generate_menu_inline(button_list))
    else:
        db_initilaze(call, parsing_words(call))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        keyboard.add('Начать')
        bot.send_message(call.message.chat.id, "Чтобы начать нажми на кнопку", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def check_message(message):
    data = load_json()
    button_list = ['Вернуться в главное меню']
    if message.text == "Начать":
        font = ImageFont.truetype('21154.otf', size=128)
        img = Image.new('RGBA', (1280, 1280), 'white')
        idraw = ImageDraw.Draw(img)
        idraw.text(
            (600, 1000),
            load_json()[str(message.chat.id)][0]["word_hiden"],
            fill=('#1C0606'), font=font
        )
        idraw.text(
            (600, 100),
            load_json()[str(message.chat.id)][0]["them"],
            fill=('#1C0606'), font=font
        )
        bot.send_message(message.chat.id, "загрузка", reply_markup=generate_keyboard(message))
        media_message = bot.send_photo(message.chat.id, pic_draw_accsess(message,step=0), reply_markup=generate_menu_inline(button_list))
        data[str(message.chat.id)][0]["message_edit"] = media_message.id
        dump_json(data)
        bot.delete_message(message.chat.id, message.message_id)
    elif len(message.text) == 1:
        data = load_json()
        bot.send_message(message.chat.id, "загрузка", reply_markup=generate_keyboard(message))
        bot.edit_message_media(media=types.InputMedia(type='photo', media=check_letters(message)),
                               chat_id=message.chat.id,
                               message_id=data[str(message.chat.id)][0]["message_edit"],
                               reply_markup=generate_menu_inline(button_list))
    elif data[str(message.chat.id)][0]["message_edit"] is None:
        bot.send_message(message.chat.id, "Подожди, игра пока не началась")
