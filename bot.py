import datetime

import time
import numpy as np
from PIL import Image
import json
from torchvision.transforms import functional as TF


import pytz
import argparse
from flask import Flask, request


from telebot import types
import tg_logger
import logging
import telebot 





import json



import numpy as np



# ------------- uptime var -------------
boot_time = time.time()
boot_date = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))

# ------------- flask config -------------
ADMIN_PASSWORD = 'admin'
app = Flask(__name__)

# ------------- bot config -------------
WEBHOOK_TOKEN = 'aa'
BOT_TOKEN = '1952171919:AAEhyxGpEcPza1Y4vN2UwkS5VqNz9U1r27c'
bot = telebot.TeleBot(BOT_TOKEN)

# ------------- log ---------------
users = ['241154130']

alpha_logger = logging.getLogger()
alpha_logger.setLevel(logging.INFO)
tg_logger.setup(alpha_logger, token="1227347441:AAEnih283opCWcQLFcbghBXc_t1tIp64QXA", users=users)
tg_logger.setup(app.logger, token="1227347441:AAEnih283opCWcQLFcbghBXc_t1tIp64QXA", users=users)

logger = logging.getLogger("tg-bot-tti")



# -------------- status webpage --------------
@app.route('/')
def status():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        logger.info('Status page loaded without password')
        return "<h1>Access denied!<h1>", 403

    return f'<h1>This is telegram bot server, ' \
           f'<a href="WTF are u doing here">templated</a> by ' \
           f'<a href="https://github.com/AlexWortega">@alexwortega</a></h1>' \
           f'<p>Server uptime: {datetime.timedelta(seconds=time.time() - boot_time)}</p>' \
           f'<p>Server last boot at {boot_date}'


# ------------- webhook ----------------
@app.route('/' + WEBHOOK_TOKEN, methods=['POST'])
def getMessage():
    temp = request.stream.read().decode("utf-8")
    temp = telebot.types.Update.de_json(temp)
    logger.debug('New message received. raw: %s', temp)
    bot.process_new_updates([temp])
    return "!", 200


@app.route("/set_webhook")
def webhook_on():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        logger.info('Set_webhook page loaded without password')
        return "<h1>Access denied!<h1>", 403

    bot.remove_webhook()
    url = 'https://' + os.environ.get('HOST') + '/' + WEBHOOK_TOKEN
    bot.set_webhook(url=url)
    logger.info(f'Webhook is ON! Url: %s', url)
    return "<h1>WebHook is ON!</h1>", 200


@app.route("/remove_webhook")
def webhook_off():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        logger.info('Remove_webhook page loaded without password')
        return "<h1>Access denied!<h1>", 403

    bot.remove_webhook()
    logger.info('WebHook is OFF!')
    return "<h1>WebHook is OFF!</h1>", 200


# --------------- bot -------------------


import re

from PIL import Image






@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    '''Displaying the bot's start interface'''

    logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used /start or /help')
    bot.send_message(message.chat.id,
                     """Это бот Text2Image разработан в СБЕР Creative AI в 2021 году. Просто отправте сообщение и я сгенерирую изображение. Например: яблоко перед камином """,
                     parse_mode='html')

import requests
from PIL import Image
from io import BytesIO
import numpy as np
import base64
from io import BytesIO

def decode_img(img_b64):
      bin_img = base64.b64decode(img_b64)
      buff = BytesIO(bin_img)
      img = np.array(Image.open(buff))
      return img

@bot.message_handler(content_types=["text"])
def process_step(message):
    text = message.text
    bot.send_message(message.chat.id,'Ваш запрос в работе')
    #try:
    
    iter = 500
    size = 450

    if len(text)>2:
        text = text
        try:
            image = model.text2image_QHM(text = text,iter = iter,rand = 0,x=size,y=size)    

            image = TF.to_pil_image(image)
            bot.send_photo(message.chat.id,image)
            logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used next:\n\n%s', message.text)
       
        except Exception as err:
            #bot.send_message(message.chat.id, str(err))
            logger.info(f'</code>@{message.from_user.username}<code> {str(err)}')
	     #torch.cuda.empty_cache()        
       
        
        
      
    




   # logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used next:\n\n%s', pic)
    
 


if __name__ == '__main__':

  #if os.environ.get("IS_PRODUCTION", "False") == "True":
    
  
   # app.run()
  #else:
#  webhook_on()
  bot.polling(none_stop=True)