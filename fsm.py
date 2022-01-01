from transitions.extensions import GraphMachine

from utils import send_text_message
req_menu_double = 'Here comes the menu!\n1.小碎步(請輸入\na 獲得詳細資訊)\n2.壓迫性發球(致勝關鍵基本功,請輸入\nb 獲得詳細資訊)\n3.(Optinal)你想不想練擊球甜蜜點手感?(Yes or No)'
req_menu_single = 'Here comes the menu!\n1.米字步(全場跑腳步的基本功,請輸入\na 獲得詳細資訊)\n2.短球、長球發球(發球基本功,請輸入\nb 獲得詳細資訊)\n3.(Optinal) 你想不想練反手擊球穩定度?(Yes or No)'
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
        req = 'OK 看來這次只有你一個人，那就來點體能訓練好了!\n但首先，告訴我你想練單打還是雙打(Single or Double?)'
        req_2 = 'OK 如果有同伴的話，訓練將更加多元! 你們想練單打還是雙打?(Single or double?)'
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    send_text_message(reply_token,req)
                else:
                    send_text_message(reply_token,req_2)
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
                    req = req_menu_single
                    break
        send_text_message(reply_token,req)
    def is_Double(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text == "Double":
            for item in users:
                if uid == item.uid:
                    item.match = 'Double'
                    break
            return True
        else:
            return False
    def Double_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    req = req_menu_double
                    break
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
                if item.number == 1 and item.match == 'Single':
                    req = '聽好喔~ 首先將球打高\n接著配合腳步移動對的位置\n最後抓時機打出長球或過渡球'
                    send_text_message(reply_token,req+req_menu_single)
                elif item.number == 1 and item.match == "Double":
                    req = 'send image'
                    send_text_message(reply_token,req+req_menu_double)
                break
        self.go_back(event)
    def is_a(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text == "a":
            return True
        else:
            return False
    def a_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1 and item.match == "Single":
                    req = 'send image of 6 point run'
                    send_text_message(reply_token,req+req_menu_single)
                elif item.number == 1 and item.match == "Double":
                    req = 'send image of small'
                    send_text_message(reply_token,req+req_menu_double)
                break
        
        self.go_back(event)
    def is_b(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text == "b":
            return True
        else:
            return False
    def b_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1 and item.match == "Single":
                    req = 'send image of basic serve'
                    send_text_message(reply_token,req+req_menu_single)
                    break
                elif item.number == 1 and item.match == "Double":
                    req = 'send image of ad serve'
                    send_text_message(reply_token,req+req_menu_double)
                    break
        
        self.go_back(event)
    def is_test(self,event):
        return True
    def test(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎使用羽球訓練菜單輔助機器人!\n請輸入總共有幾人要進行訓練!")
    def go_back_single(self,event):
        text = event.message.text
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.match == "Single":
                    return True
                else :
                    return False
    def go_back_double(self,event):
        text = event.message.text
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.match == "Double":
                    return True
                else :
                    return False