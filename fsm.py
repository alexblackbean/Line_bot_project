from transitions.extensions import GraphMachine

from utils import push_image, push_message, send_image_url, send_text_message
req_menu_double = 'Here comes the menu!\n1.小碎步(請輸入\na 獲得詳細資訊)\n2.壓迫性發球(致勝關鍵基本功,請輸入\nb 獲得詳細資訊)\n3.(Optinal)你想不想練擊球甜蜜點手感?(Yes or No)\n4.結束(end)'
req_menu_single = 'Here comes the menu!\n1.米字步(全場跑腳步的基本功,請輸入\na 獲得詳細資訊)\n2.短球、長球發球(發球基本功,請輸入\nb 獲得詳細資訊)\n3.(Optinal) 你想不想練反手擊球穩定度?(Yes or No)\n4.結束(end)'
req_menu_double_2 = 'Here comes the menu!\n1.平球互推(請輸入\na 獲得詳細資訊)\n2.殺球->接殺->平壓->起高->殺球 (請輸入\nb 獲得詳細資訊)\n3.(optional)若人數有3人以上，想不想練習比賽進攻?(Yes or No)\n4.結束(end)'
req_menu_single_2 = 'Here comes the menu!\n1.切球->放短球->放短球->挑高->切球(請輸入\na 獲得詳細資訊)\n2.切球->放短球->挑球->切球 (請輸入\nb 獲得詳細資訊)\n3.(optional)練習斜向步伐?(Yes or No)\n4.結束(end)'
users = []
ngrok_url = 'https://4377-123-194-8-218.ngrok.io'


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
        if text.lower() == "single":
            for item in users:
                if uid == item.uid:
                    item.match = 'Single'
                    break
            return True
        else:
            return False
    def Single_reply(self,event):
        
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1:
                    req = req_menu_single
                else:
                    req = req_menu_single_2
                break
        push_message(req,uid)
    def is_Double(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text.lower() == "double":
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
                else:
                    req = req_menu_double_2
                break
        send_text_message(reply_token,req)
    def is_AD(self,event):
        text = event.message.text
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if text.lower() == 'yes':
                    item.AD = True
                    return True
                else :
                    item.AD = False
                    return False
    def AD(self,event):
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1 and item.match == 'Single':
                    req = '首先將球打到非慣用手方向之高處\n接著配合腳步移動對的位置\n最後抓時機打出長球或過渡球'
                    push_message(req,uid)
                elif item.number == 1 and item.match == "Double":
                    req = '把這個套子裝在你的羽球拍上讓擊球時有阻力(訓練咬球感)'
                    img = 'https://i.imgur.com/izAK73o.jpg'
                    push_image(img,uid)
                    push_message(req,uid)
                elif item.number == 2 and item.match == 'Single':
                    img = 'https://i.imgur.com/fwPMAnq.png?1'
                    push_image(img,uid)
                elif item.number == 2 and item.match == 'Double':
                    img = 'https://i.imgur.com/tvEiKoW.png?1'
                    push_image(img,uid) 
                break
        self.go_back(event)
    def is_a(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text.lower() == "a":
            return True
        else:
            return False
    def a_reply(self,event):
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1 and item.match == "Single":
                    req = 'https://youtu.be/1d-NrsY99zk'
                    img = "https://i.imgur.com/PZB9OGZ.jpg"
                    push_message(req,uid)
                    push_image(img,uid)
                elif item.number == 1 and item.match == "Double":
                    req = 'https://youtu.be/xAUlx0eJ9eQ'
                    push_message(req,uid)
                elif item.number == 2 and item.match == "Single":
                    img = "https://i.imgur.com/AnKfCc2.png?1"
                    push_image(img,uid)
                elif item.number == 2 and item.match == "Double":
                    img = "https://i.imgur.com/4Cn49uZ.png?1"
                    push_image(img,uid)
                break
        
        self.go_back(event)
    def is_b(self,event):
        text = event.message.text
        uid = event.source.user_id
        if text.lower() == "b":
            return True
        else:
            return False
    def b_reply(self,event):
        reply_token = event.reply_token
        uid = event.source.user_id
        for item in users:
            if uid == item.uid:
                if item.number == 1 and item.match == "Single":
                    img_1 = "https://i.imgur.com/JtvQ3NM.png"
                    img_2 = "https://i.imgur.com/FBp7rIy.png"
                    img_3 = "https://i.imgur.com/elBu1yg.png"
                    push_image(img_1,uid)
                    push_image(img_2,uid)
                    push_image(img_3,uid)
                elif item.number == 1 and item.match == "Double":
                    img_1 = "https://i.imgur.com/CjUwcwS.png"
                    img_2 = "https://i.imgur.com/6rHcRZc.jpg"
                    img_3 = "https://i.imgur.com/pyutxV5.png"
                    push_image(img_1,uid)
                    push_image(img_2,uid)
                    push_image(img_3,uid)
                elif item.number == 2 and item.match == "Single":
                    img = "https://i.imgur.com/M63X62T.png?1"
                    push_image(img,uid)
                elif item.number == 2 and item.match == "Double":
                    img = "https://i.imgur.com/7dDXuq5.png?1"
                    push_image(img,uid)
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
    def is_final(self,event):
        text = event.message.text
        if text.lower() == "end":
            return True
        else:
            return False
    def good_bye(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "那就下次再使用吧~\n希望有幫助到你! (p.s. 輸入任意字串才次開始!)")