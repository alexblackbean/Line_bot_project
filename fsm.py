from transitions.extensions import GraphMachine

from utils import send_text_message
users = []
value = 0 #object
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def number_check_one(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text.lower() == '1' or text.lower() == 'one':
            print('hi')
            for item in users:
                if uid == item.uid:
                    item.number = 1
                    break
            return True
        else:
            return False
    def number_check_notone(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text.lower() == '1' or text.lower() == 'one':
            return False
        else:
            for item in users:
                if uid == item.uid:
                    item.number = 2
                    break
            return True
    def number_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        req = 'Hmm...In this case, we suggest you to do some stamaina trainning, but first, Tell us match kind!\n (Single or double?)'
        req_2 = 'Because you have partners,Please tell us what kind of match do you want to train for (Single or double?)'
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    send_text_message(reply_token,"OK you select one person\n"+req)
                else:
                    send_text_message(reply_token,"OK you select two or more\n"+req_2)
                break
    def is_Single(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text == "Single":
            for item in users:
                if uid == item.uid:
                    item.match = 'Single'
                    break
            return True
        else:
            return False
    def Single_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    req = 'Here comes the menu!\n1.米字步(全場跑腳步的基本功)\n2.短球、長球發球(發球基本功)\n3.(Optinal) 你想不想練反手擊球穩定度?(Yes or No)'
                    break
        req_f = ''
        send_text_message(reply_token,req)
    def is_AD(self,event):
        text = event.message.text
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if text == 'Yes':
                    item.AD = True
                    return True
                else :
                    item.AD = False
                    return False
    def AD(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    req = '聽好喔~ 首先將球打高\n接著配合腳步移動對的位置\n最後抓時機打出長球或過渡球'
                break
        send_text_message(reply_token,req)
    def is_test(self,event):
        return True
    def test(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Welcome to badminton trainning planner!\nPlease Enter the number of trainers!")