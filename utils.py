import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage

ngrok_url = 'https://4377-123-194-8-218.ngrok.io'
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_image_url(reply_token, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,ImageSendMessage(img_url,img_url))

def push_message(txt,id):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TextSendMessage(text=txt))
def push_image(img,id):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, ImageSendMessage(img,img))
# def send_button_message(id, text, buttons):
    # pass

