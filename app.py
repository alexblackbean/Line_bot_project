import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import fsm
from fsm import TocMachine
from utils import send_text_message

load_dotenv()
# machine = TocMachine(
#                 states=["initial","number","one", "not_one"],
#                 transitions=[
#                     {
#                         "trigger": "advance",
#                         "source": "initial",
#                         "dest": "number",
#                         "conditions": "is_test",
#                         "before": "test"
#                     },
#                     {
#                         "trigger": "advance",
#                         "source": "number",
#                         "dest": "one",
#                         "conditions": "number_check_one",
#                         "after": "number_reply"   
#                     },
#                     {
#                         "trigger": "advance",
#                         "source": "number",
#                         "dest": "not_one",
#                         "conditions": "number_check_notone",
#                         "after": "number_reply"   
#                     },

#                 ],
#                 initial="initial",
#                 auto_transitions=False,
#                 show_conditions=True,
#             )
machine = TocMachine(
            states=["initial","number","one", "not_one","Single","Double","AD","a","b"],
            transitions=[
                {
                    "trigger": "advance",
                    "source": "initial",
                    "dest": "number",
                    "conditions": "is_test",
                    "before": "test"
                },
                {
                    "trigger": "advance",
                    "source": "number",
                    "dest": "one",
                    "conditions": "number_check_one",
                    "after": "number_reply"   
                },
                {
                    "trigger": "advance",
                    "source": "number",
                    "dest": "not_one",
                    "conditions": "number_check_notone",
                    "after": "number_reply"   
                },
                {
                    "trigger": "advance",
                    "source": ["one","not_one"],
                    "dest": "Single",
                    "conditions": "is_Single",
                    "after": "Single_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "AD",
                    "conditions": "is_AD",
                    "after": 'AD'
                },
                {
                    "trigger": "advance",
                    "source": ["one","not_one"],
                    "dest": "Double",
                    "conditions": "is_Double",
                    "after": "Double_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "a",
                    "conditions": "is_a",
                    "after": "a_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "b",
                    "conditions": "is_b",
                    "after": "b_reply"
                },
                {
                    "trigger": "go_back",
                    "source": ["a","b","AD"],
                    "dest": "Single",
                    "conditions": "go_back_single",
                    "after": "Single_reply"
                },
                {
                    "trigger": "go_back",
                    "source": ["a","b","AD"],
                    "dest": "Double",
                    "conditions": "go_back_double",
                    "after": "Double_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "initial",
                    "conditions": "is_final",
                    "after": "good_bye"
                }

            ],
            initial="initial",
            auto_transitions=False,
            show_conditions=True,
        )
class User():
    def __init__(self):
        self.uid = 0
        self.machine = 0
        self.number = 0
        self.match = ''
        self.AD = False

app = Flask(__name__, static_url_path="")

first_time = True
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    # parse webhook body
    try:
        events = parser.parse(body, signature)
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        user_id = event.source.user_id
        flag = False
        temp = None
        for item in fsm.users:
            if item.uid == user_id:
                flag = True
                temp = item.machine
                break
        if flag == True:
            response = temp.advance(event)
            print(temp.state)
            if response == False:
                send_text_message(event.reply_token, "可能指令輸入錯了喔~~ 再輸入一次")

    return "OK"
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    found = False
    global first_time
    if not first_time:
        for item in fsm.users:
            if item.uid == user_id:
                found = True
                break
    else:
        first_time = False
        found = False
    if not found:
        new_user = User()
        new_user.uid = user_id
        new_user.machine = TocMachine(
            states=["initial","number","one", "not_one","Single","Double","AD","a","b"],
            transitions=[
                {
                    "trigger": "advance",
                    "source": "initial",
                    "dest": "number",
                    "conditions": "is_test",
                    "before": "test"
                },
                {
                    "trigger": "advance",
                    "source": "number",
                    "dest": "one",
                    "conditions": "number_check_one",
                    "after": "number_reply"   
                },
                {
                    "trigger": "advance",
                    "source": "number",
                    "dest": "not_one",
                    "conditions": "number_check_notone",
                    "after": "number_reply"   
                },
                {
                    "trigger": "advance",
                    "source": ["one","not_one"],
                    "dest": "Single",
                    "conditions": "is_Single",
                    "after": "Single_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "AD",
                    "conditions": "is_AD",
                    "after": 'AD'
                },
                {
                    "trigger": "advance",
                    "source": ["one","not_one"],
                    "dest": "Double",
                    "conditions": "is_Double",
                    "after": "Double_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "a",
                    "conditions": "is_a",
                    "after": "a_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "b",
                    "conditions": "is_b",
                    "after": "b_reply"
                },
                {
                    "trigger": "go_back",
                    "source": ["a","b","AD"],
                    "dest": "Single",
                    "conditions": "go_back_single",
                    "after": "Single_reply"
                },
                {
                    "trigger": "go_back",
                    "source": ["a","b","AD"],
                    "dest": "Double",
                    "conditions": "go_back_double",
                    "after": "Double_reply"
                },
                {
                    "trigger": "advance",
                    "source": ["Single","Double"],
                    "dest": "initial",
                    "conditions": "is_final",
                    "after": "good_bye"
                }

            ],
            initial="initial",
            auto_transitions=False,
            show_conditions=True,
        )
        fsm.users.append(new_user)

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
