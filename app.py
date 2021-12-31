import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

class User():
    def __init__(self):
        self.uid = 0
        self.machine = None
# machine = TocMachine(
#     states=["user", "state1", "state2"],
#     transitions=[
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state1",
#             "conditions": "is_going_to_state1",
#         },
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state2",
#             "conditions": "is_going_to_state2",
#         },
#         {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
#     ],
#     initial="user",
#     auto_transitions=False,
#     show_conditions=True,
# )

app = Flask(__name__, static_url_path="")
users = []
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
    # if 'userid'
    app.logger.info(f"Request body: {body}")
    # parse webhook body
    try:
        events = parser.parse(body, signature)
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    # if event is MessageEvent and message is TextMessage, then echo text
    # print(len(users))
    for event in events:
        user_id = event.source.user_id
        flag = False
        temp = None
        for item in users:
            if item.uid == user_id:
                flag = True
                temp = item.machine
                break
        # if not isinstance(event, MessageEvent):
        #     continue
        # if not isinstance(event.message, TextMessage):
        #     continue
        # if not isinstance(event.message.text, str):
        #     continue
        # print(f"\nFSM STATE: {machine.state}")
        # print(f"REQUEST BODY: \n{body}")
        if flag == True:
            response = temp.advance(event)
            if response == False:
                send_text_message(event.reply_token, "Not Entering any State")

    return "OK"
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    found = False
    global first_time
    if not first_time:
        for item in users:
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
                states=["user", "state1", "state2"],
                transitions=[
                    {  
                        "trigger": "advance",
                        "source": "user",
                        "dest": "state1",
                        "conditions": "is_going_to_state1",
                    },
                    {
                        "trigger": "advance",
                        "source": "user",
                        "dest": "state2",
                        "conditions": "is_going_to_state2",
                    },
                    {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
                ],
                initial="user",
                auto_transitions=False,
                show_conditions=True,
            )
        users.append(new_user)
        # print('user_id = ', user_id)

# @app.route("/webhook", methods=["POST"])
# def webhook_handler():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info(f"Request body: {body}")

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue
#         if not isinstance(event.message.text, str):
#             continue
#         print(f"\nFSM STATE: {machine.state}")
#         print(f"REQUEST BODY: \n{body}")
#         response = machine.advance(event)
#         machin
#         if response == False:
#             send_text_message(event.reply_token, "Not Entering any State")

#     return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
