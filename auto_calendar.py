import epd7in5
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import re
import glob
import os
import random
from itertools import chain

#パラメータ調整用、気象庁で表示している県コード
weather_ken_cd = "315" #群馬県
weather_row = 0

def get_font(size, font="ipaexg.ttf"):
    return ImageFont.truetype(font, size)

def select_image():
    if not os.path.isdir("img"):
        return "noimage.jpg"
    ext_list = ["bmp", "jpg", "png"]
    images = list(chain.from_iterable([glob.glob("img/*." + ext) for ext in ext_list]))
    if len(images) == 0:
        return "noimage.jpg"
    i = random.randint(0, len(images) - 1)
    return images[i]
 
def draw_image(image):
    print("Draw image.")
    path = select_image()
    if not os.path.exists(path):
        return
    bg = Image.open(path)
    #画面左側に画像を表示
    rate = min(360 / bg.width, eh / bg.height)
    #明るさ調整する場合は下記のコードを有効にする
    #bg = bg.point(lambda x: x * 1.2)
    #リサイズ
    bg = bg.resize(((int)(bg.width * rate), (int)(bg.height * rate)))
    image.paste(bg, (ew - bg.width, (int)((eh - bg.height) / 2)))

def draw_today(g):
    print("Draw today")
    now = datetime.now()
    g.text((0, 0), now.strftime("%Y年 %m月"), font = get_font(36), fill = 0)
    g.text((0, 50), now.strftime("%d"), font = get_font(128), fill = 0)
    g.text((180, 120), "日", font = get_font(48), fill = 0)
    i = now.weekday()
    s = "月火水木金土日"[i]
    g.text((170, 50), "({})".format(s), font = get_font(64), fill = 0)

def draw_weather(g, ken, row):
    #気象庁の明日の天気予報を取得
    print("Draw weather.")
    src = requests.get('http://www.jma.go.jp/jp/yoho/{0}.html'.format(ken)).text
    if datetime.today().hour < 13:
        s = "今日"
    else:
        s = "明日"
    th = re.findall('<th class="weather">.*?{}(\d+)日.+? title="(.+?)"(.+?)</table>'.format(s), src, flags=(re.MULTILINE | re.DOTALL))
    day = th[row][0]
    g.text((0, 190), "{}日の天気：".format(day), font = get_font(24), fill = 0)
    weather = th[row][1]
    size = 48
    if len(weather) > 5:
        size = 36
    g.text((30, 220), weather, font = get_font(size), fill = 0)
    tbl = re.findall('<td align="left"( nowrap)?>(.+?)</td>.<td align="right">(.+?)</td>', th[row][2], flags=(re.MULTILINE | re.DOTALL))
    hours = [m[1] for m in tbl]
    certs = [m[2].rjust(5) for m in tbl]
    g.text((0, 280), " ".join(hours), font = get_font(20, "FreeMono.ttf"), fill = 0)
    g.text((0, 300), "/".join(certs), font = get_font(20, "FreeMono.ttf"), fill = 0)
    #print("/".join(certs))

def draw_fortune(g):
    print("Draw fortune")
    if not os.path.isfile("fortune.txt"):
        return
    with open("fortune.txt", "r", encoding="utf-8") as f:
        text = f.read()
        ms = re.findall("^%(.+)$", text, flags=(re.MULTILINE))
        if not ms:
            return
        i = random.randint(0, len(ms) - 1)
        s = ms[i]
        print(s)
        g.text((0, 330), s, font = get_font(20), fill=0)

def draw_update(g):
    now = datetime.now()
    s = "更新日時: {0:%Y-%m-%d %H:%M:%S}".format(now)
    g.text((65, 360), s, font = get_font(14), fill=0)

epd = epd7in5.EPD()
epd.init()
print("Width: %d, Height: %d" % (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT))

ew = epd7in5.EPD_WIDTH
eh = epd7in5.EPD_HEIGHT
image = Image.new('1', (ew, eh), 1) # 1: clear the frame
draw_image(image)
g = ImageDraw.Draw(image)
draw_today(g)
draw_weather(g, weather_ken_cd, weather_row)
draw_fortune(g)
draw_update(g)
epd.display_frame(epd.get_frame_buffer(image))

