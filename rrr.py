from parametrs import headers
import json
from PIL import Image, ImageDraw, ImageFont
import re
import io
from transliterate import translit
from telebot import types
import os
from bs4 import BeautifulSoup
import requests
import random
import numpy as np
def generate_menu_inline(button_list):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for button in button_list:
        keyboard.add(types.InlineKeyboardButton(translit(button,'ru'), callback_data=button))
    return keyboard

def generate_keyboard(message):
    data = load_json()
    data = data[str(message.chat.id)][0]["word_hiden"]
    button_list = [chr(i) if chr(i) not in list(data) else "❌" for i in range(1072,1104)]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in button_list:
        keyboard.add(types.InlineKeyboardButton(button))
    print(keyboard)
    return keyboard
def load_json():
    print("ddd")
    with open('word.json','r', encoding='utf-8') as f:
        data = json.load(f)
        print(data)
        return data

def dump_json(data):
    with open('word.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def check_letters(message):
    data = load_json()
    word = data[str(message.chat.id)][0]["word"]
    if message.text in word:
        word_hiden = list(data[str(message.chat.id)][0]["word_hiden"])
        count_find = [m.start() for m in re.finditer(message.text, word)]
        for i in count_find:
            word_hiden[i] = message.text
        data[str(message.chat.id)][0]["word_hiden"] = "".join(word_hiden)
        dump_json(data)
        step = data[str(message.chat.id)][0]["step"]
        return pic_draw_accsess(message,step)
    else:
        data[str(message.chat.id)][0]["step"] += 1
        dump_json(data)
        step = data[str(message.chat.id)][0]["step"] + 1
        return pic_draw_accsess(message,step)

def pic_draw_accsess(message,step):
    if step != 7:
        font = ImageFont.truetype('21154.otf', size=128)
        img = Image.new('RGBA', (1280, 1280), 'white')
        for i in range(1, step):
            with Image.open(f"media/{i}.png").convert("RGBA") as step_img:
                img.paste(step_img,step_img)
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
        try:
            with io.BytesIO() as buf:
                img.save(buf, 'png')
                image_bytes = buf.getvalue()
            return image_bytes
        except:
            pass
    else:
        ...
def db_initilaze(call,word):
    if os.path.exists("word.json"):
        data = load_json()
        data[call.message.chat.id] = []
        data[call.message.chat.id].append(
            {'word': word, 'them': translit(call.data, 'ru'), 'step': 0, 'word_hiden': len(word) * '_', 'message_edit': None})
        dump_json(data)
    else:
        data = {}
        data[call.message.chat.id] = []
        data[call.message.chat.id].append(
            {'word': word, 'them': translit(call.data, 'ru'), 'step': 0, 'word_hiden': len(word) * '_', 'message_edit': None})
        dump_json(data)

def parsing_words(call):
    data = requests.get(f"http://rus.lang-study.com/category/slovar/{str(call.data)}/", headers=headers)
    soup = BeautifulSoup(data.text, "html5lib")
    soup = soup.find_all('h3', class_='title')
    word = [word.text for word in soup]
    word = random.choice(word).lower()
    return word