from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('7zpP4zMvdkNu6APM8eQC0tt/170U8EJo3fuEBKoB20IB+J+BZtbz6UXeBDt2zpIWCcbRHGtW8e+8oo/0Vgrd+Wc2bbqED8jTAsk/Xoqp73LV8MLiGT2ZMf/zC4NQX9OKqUVJUddVNlBQSl9t1zD4WgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('1994341e5ad9e5a5482de603ccd7ae04')
#===========[ NOTE SAVER ]=======================
notes = {}

mimic = {
    "target":{}
}

helpmessage = """[ บอทสาธารณะ ] เวอร์ชั่น 0.7.1
* โค้ดหนึ่งใช้ได้ 100 คำสั่ง
╭━━━━━━━━━━━━━━━━╮
┃               คำสั่งปกติ
╰━━━━━━━━━━━━━━━━╯
- /profile โปรไฟล์
- /id ไอดี
- /bio ข้อความสถานะ
- /name ชื่อ
- /pic รูปโปรไฟล์
- /idline [ ไอดีไลน์ ]
สร้างลิงก์แอดเพื่อน
- /contact ติดต่อ

╭━━━━━━━━━━━━━━━━╮
┃               คำสั่งพิเศษ
╰━━━━━━━━━━━━━━━━╯
- /spam [ จำนวน ] [ ข้อความ ]
- /shorturl [ URL ] ย่อ URL
- /check [ ไอดี URL ] ข้อมูล URL
- /news [ ประเทศ ] *ตัวย่อเท่านั้น
- /yt [ query ] ยูทูป
- /wiki [ query ] วิกิพีเดีย
- /weather สภาพอากาศ
- /share ดูหุ้น

╭━━━━━━━━━━━━━━━━╮
┃           คณิตศาสตร์
╰━━━━━━━━━━━━━━━━╯
- /plus [ ตัวเลข ] [ ตัวเลข ] บวก
- /minus [ ตัวเลข ] [ ตัวเลข ] ลบ
- /divide [ ตัวเลข ] [ ตัวเลข ] หาร
- /mtp [ ตัวเลข ] [ ตัวเลข ]  คูณ
- /mtpt [ ตัวเลข ] สูตรคูณ
- /sqrt [ ตัวเลข ] สแควรูท

╭━━━━━━━━━━━━━━━━╮
┃       คำสั่งเฉพาะแอดมิน
╰━━━━━━━━━━━━━━━━╯
- /bye บอทออก

╭━━━━━━━━━━━━━━━━╮
┃                 เร็วๆ นี้
╰━━━━━━━━━━━━━━━━
- /ptgr [ ตัวเลข ] [ ตัวเลข ]
- /graph [[ x ],[ y ]] กราฟ

ติดต่อแอดมิน line.me/ti/p/~esci_"""

groupcast = {}
code = {}
veri = {}
codx = {}
#groupcastt = "no"
groupcastt = "ระบบจะปิดอัตโนมัติในวันที่ 31 กันยายน 2561 เวลา 25:00 นาฬิกา"

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='สวัสดี พิพม์ /help เพื่อดูคำสั่งทั้งหมด',quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label="กดที่นี่เพื่อดูคำสั่งทั้งหมด", text="/help"))])))
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
    try:
        if veri[gid] == True:
            codex[gid] = codex[gid] + 1
    except:
        veri[gid] = False
        codex[gid] = 0
    try:
        if veri[gid] == True:
            if codex[gid] == 5:
                line_bot_api.push_message(gid, TextSendMessage(text="โค้ดหมดอายุแล้ว"))
                veri[gid] = False
                codex[gid] = 0
    except:
        veri[gid] = False
        codex[gid] = 0
    if text.startswith("/verify"):
        try:
            if veri[gid] == True:
                line_bot_api.push_message(gid, TextSendMessage(text="บอทได้รับการยืนยันเรียบร้อยแล้ว"))
            else:
                try:
                    separate = text.split(" ")
                    search = text.replace(separate[0] + " ","")
                    if search == code[gid]:
                        line_bot_api.push_message(gid, TextSendMessage(text="ยืนยันสำเร็จ"))
                        veri[gid] = True
                    else:
                        line_bot_api.push_message(gid, TextSendMessage(text="โค้ดยืนยันไม่ถูกต้อง"))
                except:
                    return
        except:
            veri[gid] = False
            line_bot_api.push_message(gid, TextSendMessage(text="บอทได้รับการยืนยันเรียบร้อยแล้ว"))
    if text.startswith("/"):
        try:
            if veri[gid] == False:
                n = ["1","2","3","4","5","6","7","8","9","0","A","B","C","D","E","F","G"]
                b = ""
                for x in range(5):
                    b+=random.choice(n)
                try:
                    code[gid] = b
                    line_bot_api.push_message(gid, TextSendMessage(text="พิพม์ /verify " + code[gid] + "\nเพื่อยืนยันบอท"))
                    return
                except:
                    code[gid] = b
                    line_bot_api.push_message(gid, TextSendMessage(text="พิพม์ /verify " + code[gid] + "\nเพื่อยืนยันบอท"))
                    return
        except:
            code[gid] = ""
            veri[gid] = False
            return
    if groupcastt != "no":
        try:
            if groupcast[gid] == False:
                groupcast[gid] = True
                h = "[ ประกาศ ]\n\n" + groupcastt
                line_bot_api.push_message(gid, TextSendMessage(text=h))
        except:
            groupcast[gid] = False
    """if text.startswith("/broadcast"):
        separate = text.split(" ")
        textt = text.replace(separate[0] + " ","")
        if(event.source.user_id == "Udaa0a2f396dd41e4398b106d903d92fd"):
            line_bot_api.reply_message(gid, TextSendMessage(text="ตั้งข้อความประกาศว่า " + textt))
            groupcastt = textt
            groupcast = {}
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ผู้ใช้นี้ไม่ได้รับอนุญาต"))	"""	
    #try:
    #    if groupcast[gid] == True:
    #        line_bot_api.push_message(gid, TextSendMessage(text="[ ประกาศ ]\n"+groupcastt))
    #        groupcast[gid] = False
    #    elif groupcast[gid] == False:
    #        groupcast = False
    #    else:
    #        line_bot_api.push_message(gid, TextSendMessage(text="[ ประกาศ ]\n"+groupcastt))
    #        groupcast[gid] = True
    #except Exception as Error:
    #    groupcast[gid] = False
    #    line_bot_api.push_message(gid, TextSendMessage(text="[ ประกาศ ]\n"+groupcastt))
    try:
        if veri[gid] == True:
            if text.isdigit():
                b = int(text)
                reverse = 0
                while(b > 0):
                    reminder = b %10
                    reverse = (reverse *10) + reminder
                    b = b //10
                x = int(text) + 1
                line_bot_api.push_message(gid, TextSendMessage(text=x))
    except:
        veri[gid] = False
    """if text.startswith("/graph"):
        try:
            headers = {"Authorization": "Bearer ya29.GlsMBisE2cNscXj8RW1UP32SVEkIOJ8z1rx4oE2tQGRXxomt1t6rxoM9L11EH3pm5mKK3uIlxfytEuwN3y-4uM0eoMsFo8BjpQglayMH1E-0y5tNW0wwr4MP2nc4"}
            x = [1,2,3]
            y = [2,4,1]
            plt.plot(x, y)
            plt.xlabel('x - axis')
            plt.ylabel('y - axis')
            plt.title('[ By PASUNx ]')
            plt.savefig('b.png', dpi=100)
            para = {
                "name": "b.png",
                "parents": ["1ohcThxOTwMY-wLeP4UWaBTf_Dc7Fyr-b"]
            }
            files = {
                'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                'file': open("./b.png", "rb")
            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )
            t = r.json()
            txt = "https://drive.google.com/file/d/" + t["id"] + "/view"
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except Exception as Err:
            line_bot_api.push_message(gid, TextSendMessage(text="THIS IS BETA"))"""
    if text.startswith("/weather"):
        weatherurl = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22bangkok%2C%20th%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
        req = requests.get(weatherurl)
        x = req.json()
        aa = x["query"]["results"]["channel"]["location"]
        ab = x["query"]["results"]["channel"]["wind"]
        ac = x["query"]["results"]["channel"]["atmosphere"]
        ad = x["query"]["results"]["channel"]["astronomy"]
        b = aa["city"]
        c = ab["chill"]
        d = ab["direction"]
        e = ab["speed"]
        f = ac["humidity"]
        g = ac["pressure"]
        h = ac["rising"]
        i = ac["visibility"]
        j = ad["sunrise"]
        k = ad["sunset"]
        o = str((int(c) - 32)/1.8)
        o = o[:o.index('.')]
        txt = "สภาพอากาศ กรุงเทพมหานคร" +"\n──────────────\n"
        txt+="อุณหถูมิ " + o + " ℃"
        txt+="\nลม\nความเย็น " + c
        txt+="\nทิศทาง " + d
        txt+="\nความเร็ว " + e + " mph"
        txt+="\n\nบรรยากาศ\nความชื้น " + f
        txt+="\nความดัน " + g + " in"
        txt+="\nที่เพิ่มสูงขึ้น " + h
        txt+="\nความชัดเจน " + i
        txt+="\n\nพระอาทิตย์ขึ้น " + j
        txt+="\nพระอาทิตย์ตกดิน " + k
        line_bot_api.push_message(gid, TextSendMessage(text=txt))
    if text.startswith("/divide"):
        separate = text.split(" ")
        try:
            t1 = int(text.split(" ")[1])
            t2 = int(text.split(" ")[2])
            txt = str(t1) + " / " + str(t2) + "\n──────────────"
            txt+="\n" + str(t1 / t2)
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/divide [ ตัวเลข ] [ ตัวเลข ]"))
    if text.startswith("/plus"):
        separate = text.split(" ")
        try:
            t1 = int(text.split(" ")[1])
            t2 = int(text.split(" ")[2])
            txt = str(t1) + " + " + str(t2) + "\n──────────────"
            txt+="\n" + str(t1 + t2)
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/plus [ ตัวเลข ] [ ตัวเลข ]"))
    if text.startswith("/minus"):
        separate = text.split(" ")
        try:
            t1 = int(text.split(" ")[1])
            t2 = int(text.split(" ")[2])
            txt = str(t1) + " - " + str(t2) + "\n──────────────"
            txt+="\n" + str(t1 - t2)
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/minus [ ตัวเลข ] [ ตัวเลข ]"))
    if text.startswith("/sqrt"):
        separate = text.split(" ")
        try:
            m = int(text.replace(separate[0] + " ",""))
            txt = "สแควรูท " + str(m) + "\n──────────────"
            txt+="\n" + str(math.sqrt(m))
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/sql [ ตัวเลข ]"))

    if text.startswith("/mtpt"):
        separate = text.split(" ")
        try:
            m = int(text.replace(separate[0] + " ",""))
            txt = "สูตรคูณแม่ " + str(m) + "\n──────────────"
            for i in range(12):
	            x = i+1
	            txt+="\n" + str(m) + " * " + str(x) + " = " + str(m * x)
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/mtpt [ ตัวเลข ]"))
    elif text.startswith("/mtp"):
        separate = text.split(" ")
        try:
            t1 = int(text.split(" ")[1])
            t2 = int(text.split(" ")[2])
            txt = str(t1) + " * " + str(t2) + "\n──────────────"
            txt+="\n" + str(t1 * t2)
            line_bot_api.push_message(gid, TextSendMessage(text=txt))
        except:
            line_bot_api.push_message(gid, TextSendMessage(text="วิธีการใช้งาน:\n/mtp [ ตัวเลข ] [ ตัวเลข ]"))
    if text.startswith("/spam "):
        separate = text.split(" ")
        texxt = text.replace(separate[0] + " ","")
        textt = texxt.replace(separate[1] + " ","")
        textx = "จำนวน " + separate[1] + "\nข้อความ " + textt
        line_bot_api.push_message(gid, TextSendMessage(text=textx))
        try:
            x = int(separate[1])
            if x < 21:
                for i in range(x):
                    line_bot_api.push_message(gid, TextSendMessage(text=textt))
            else:
                line_bot_api.push_message(gid, TextSendMessage(text="ไม่สามารถสแปมมากกว่า 20 ข้อความได้"))
        except:
            pass
    if text == "/group":
        member_ids_res = line_bot_api.get_group_member_ids(group_id)
        line_bot_api.push_message(gid, member_ids_res.member_ids)
        line_bot_api.push_message(gid, member_ids_res.next)
    if text.startswith("/yt"):
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
        data = url.json()
        no = 0
        result = "ยูทูป ( ค้นหา " + search + " )\n──────────────"
        for anu in data["videos"]:
            no += 1
            result += "\n{}. {}\n{}\n".format(str(no),str(anu["title"]),str(anu["webpage"]))
        result += "\nทั้งหมด {}".format(str(len(data["videos"])))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if text.startswith("/news"):
        try:
            separate = text.split(" ")
            country = text.replace(separate[0] + " ","")
            if(country == None):country == "th"
            user_agent = {'User-agent': 'Mozilla/5.0'}
            url = requests.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=763b6fc67a594a4e9e0f9d29303f83dd".format(country))
            data = url.json()
            result="ข่าวใหม่ ( " + country.upper() + " )" + "\n──────────────"
            n = 0
            for anu in data["articles"]:
                if len(result) > 500:
                    result+="\nทั้งหมด {}".format(n)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
                else:
                    n = n + 1
                    result+="\n" + anu["title"] + "\n"+anu["url"]+"\n"
            result+="\nทั้งหมด {}".format(n)
            line_bot_api.push_message(gid, TextSendMessage(text=result))
        except Exception as Error:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Error))
    if text.startswith("/share"):
        quandl.ApiConfig.api_key = 'sSGoP_R7-sNMXusmJr7p'
        data = quandl.get("THAISE/INDEX")
        line_bot_api.push_message(gid, TextSendMessage(text=data))
    if text.startswith("/snews"):
        separate = text.split(" ")
        searchx = text.replace(separate[0] + " ","")
        search = searchx
        gs = goslate.Goslate()
        search = gs.translate(searchx,'en')
        r = requests.get("http://www.google.co.th/search?q="+search+"&tbm=nws")
        content = r.text
        news_summaries = []
        soup = BeautifulSoup(content, "html.parser")
        st_divs = soup.findAll("div", {"class": "st"})
        g_divs = soup.findAll("div", {"class": "g"})
        trs="ข่าวเกี่ยวกับ " + searchx + "\n──────────────"
        news_d = []
        for g_div in g_divs: 
            news_d.append(g_div.text)
        for st_div in st_divs:
            news_summaries.append(st_div.text)
        for i in news_summaries:
            for x in news_d:
                try:
                    if len(trs) > 600:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
                    else:
                        gs = goslate.Goslate()
                        x = gs.translate(x,'th')
                        trs+="\n\n"+x+"\nอ่านเพิ่มเติมได้ที่"
                except Exception as error:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
    if text == "/bye":
        if(event.source.user_id == "Udaa0a2f396dd41e4398b106d903d92fd"):
            confirm_template_message = TemplateSendMessage(
                alt_text='God message',
	    		template=ConfirmTemplate(
                    text='จะลบบอทออก? คุณแน่ใจหรือ?',
                    actions=[
                        PostbackAction(
                            label='แน่ใจ',
                            text='goodbye',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='ไม่',
                            text='...'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ผู้ใช้นี้ไม่ได้รับอนุญาต"))
    if "/ti/g/" in text:
        link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
        links = link_re.findall(text)
        n_links = []
        for l in links:
            if l not in n_links:
                n_links.append(l)
        for ticket_id in n_links:
            line_bot_api.push_message(gid, TextSendMessage(text="Joined"))
            line_bot_api.acceptGroupInvitationByTicket(gid,ticket_id)
    if text == '/contact':
        buttons_template_message = TemplateSendMessage(
            alt_text='God message',
            template=ButtonsTemplate(
                thumbnail_image_url='https://gamingroom.co/wp-content/uploads/2017/11/CyCYOArUoAA2T6d.jpg',
                title='ติดต่อ',
                text='ช่องทางการติดต่อ',
                actions=[
                    PostbackAction(
                        label='ไลน์',
                        text='http://line.me/ti/p/~esci_',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label="เฟซบุ๊ค",
                        text='https://www.facebook.com/pasun.cf'
                    ),
                    URIAction(
                        label='ติดต่อ',
                        uri='http://line.me/ti/p/~esci_'
                    )
                ]
            )
        )
        line_bot_api.push_message(gid, buttons_template_message)
    if '/wiki ' in text:
        try:
            wiki = text.replace("/wiki ","")
            wikipedia.set_lang("th")
            pesan="วิกิพีเดียเกี่ยวกับ "
            pesan+=wikipedia.page(wiki).title
            pesan+="\n\n"
            pesan+=wikipedia.summary(wiki, sentences=1)
            pesan+="\n\nอ่านเพิ่มเติม\n"
            pesan+=wikipedia.page(wiki).url
            titlex = wikipedia.page(wiki).title
            textx = wikipedia.summary(wiki, sentences=1)
            urlx = wikipedia.page(wiki).url
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
        except:
            try:
                pesan="เกินขีด จำกัด ข้อความ! โปรดคลิกลิงก์ข้างล่างเพื่ออ่านเพิ่มเติม\n"
                pesan+=wikipedia.page(wiki).url
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(e)))
    if text == "/kick":
        line_bot_api.kickoutFromGroup(0, gid, "Udaa0a2f396dd41e4398b106d903d92fd")
    if text == "/profile":
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.push_message(gid,TextSendMessage(text=event.source.user_id))
        line_bot_api.push_message(gid,TextSendMessage(text=profile.display_name))
        line_bot_api.push_message(gid,TextSendMessage(text=profile.status_message))
        line_bot_api.push_message(gid,TextSendMessage(text=profile.picture_url))
    if text == '/id':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/bio':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/pic':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/name':
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == 'goodbye':
        if(event.source.user_id == "Udaa0a2f396dd41e4398b106d903d92fd"):
            if isinstance(event.source, SourceGroup):
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text='กำลังออกกลุ่ม...'))
                    line_bot_api.leave_group(event.source.group_id)
            elif isinstance(event.source, SourceRoom):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='กำลังออกกลุ่ม...'))
                line_bot_api.leave_room(event.source.room_id)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="บอทไม่สามารถออกแชท 1:1 ได้"))
    
    elif "/idline " in event.message.text:
        skss = event.message.text.replace('/idline ', '')
        sasa = "http://line.me/R/ti/p/~" + skss
        text_message = TextSendMessage(text=sasa)
        line_bot_api.reply_message(event.reply_token, text_message)
    elif text.startswith('/check'):
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://shorturlbyzefyrinusx.000webhostapp.com/api/check.php?id=" + originURL + "&type=api").text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    elif text.startswith('/shorturl'):
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://shorturlbyzefyrinusx.000webhostapp.com/api/urlshorten.php?url=" + originURL).text
        buttons_template_message = TemplateSendMessage(
            alt_text='God message',
            template=ButtonsTemplate(
                thumbnail_image_url='https://gamingroom.co/wp-content/uploads/2017/11/CyCYOArUoAA2T6d.jpg',
                title='RESULT',
                text=result,
                actions=[
                    PostbackAction(
                        label='ข้อมูล URL',
                        text='/check ' + result,
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label="URL",
                        text=result
                    ),
                    URIAction(
                        label='เปิด URL',
                        uri=result
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
		
    elif '/help' == text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=helpmessage))
		
    elif '/test' == text:
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='God message',
                actions=[
                    PostbackAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
	











#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
