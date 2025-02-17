import configparser
import os
import random
import time
from datetime import date, datetime, timedelta

import math
import requests
import zhdate
from bs4 import BeautifulSoup
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

"""
1、从配置文件中获取变量
"""
conf = configparser.ConfigParser()
config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read('config.conf', 'utf8')
today = datetime.now() + timedelta() + timedelta()
start_date = conf.get("info", "start_date")  # 在一起开始日期,格式 ****-**-**
city1 = conf.get("info", "city1")  # 所在的城市(请写具体城市，如昆明)，用于匹配天气预报和热点新闻
city2 = conf.get("info", "city2")
birthday_lover = conf.get("info", "birthday_lover")  # 生日 格式**-**
birthday_my = conf.get("info", "birthday_my")
app_id = conf.get("info", "app_id")  # 微信测试号ID（开通以后自动生成）
app_secret = conf.get("info", "app_secret")  # 微信测试号密钥（开通以后自动生成）
template_id = conf.get("info", "template_id")
# 接收消息的用户ID，让你的女朋友扫微信测试号的二维码，获取微信用户ID
user_id = conf.get("info", "user_id")  # 接收消息的微信号，注意这个不是普通微信号，需要扫微信测试号后台的二维码来获取
user_id1 = user_id.split(",")

"""
2、定义获取数据的函数

"""


def get_morning_words():
    morning_inspirations = [
        "今天会是美好的一天！",
        "早晨的阳光是新的开始。",
        "新的挑战，新的机遇。",
        "早起一小时，赢得一天。",
        "每天进步一点点，成功就不远。",
        "相信自己，未来无限可能。",
        "你比你想象的更强大。",
        "保持微笑，迎接新的一天。",
        "今天是你改变的最佳时机。",
        "让今天成为最棒的一天！",
        "不畏将来，不念过往。",
        "做自己，做最好的自己。",
        "每天都是新的机会。",
        "努力不一定会成功，但放弃一定会失败。",
        "勇敢面对每一个晨曦。",
        "新的一天，新的开始。",
        "人生没有彩排，每一天都是现场直播。",
        "保持信念，迎接每个晨光。",
        "未来属于那些努力的人。",
        "阳光明媚，心情也跟着好！",
        "清晨就是新的开始，勇敢去追逐梦想。",
        "每天醒来，都是新的机会。",
        "新的一天，新的希望，继续加油！",
        "给自己一个微笑，开始新的一天。",
        "挑战自己，迎接美好的一天。",
        "阳光明媚，心情也跟着明亮。",
        "从早晨开始，做最好的自己。",
        "每天都是全新的机会，抓住它！",
        "今天做更好的自己，明天更精彩。",
        "每一天都充满可能性，加油！",
        "勇敢向前，未来属于你。",
        "梦想从清晨开始，努力就不晚。",
        "你今天的努力，决定明天的精彩。",
        "从晨曦中汲取力量，迎接每一天。",
        "为美好的明天而努力，今天开始！",
        "新的开始，新的挑战，新的胜利！",
        "迎接新的一天，充满正能量。",
        "今天的努力，给明天铺路。",
        "每天都是新的希望，做最好的自己。",
        "无论如何，早起的鸟儿有虫吃！"
    ]

    # 随机选择一句话
    random_inspiration = random.choice(morning_inspirations)
    return random_inspiration


def get_eatmorning_words():
    list = [
        "中午好！愿你今日心情超棒",
        "午安，祝你午餐美味又开心",
        "中午到啦，愿你生活甜如蜜",
        "中午好呀，愿幸运时刻相随",
        "午间愉快，愿身心自在轻松",
        "中午安好，愿工作一切顺利",
        "中午好，愿午后时光很惬意",
        "午安！愿你享受惬意中午",
        "中午时分，愿快乐常围绕你",
        "中午好，愿笑容时刻挂嘴边",
        "中午好！愿你今日心情超棒",
        "午安，祝你午餐美味又开心",
        "中午到啦，愿你生活甜如蜜",
        "中午好呀，愿幸运时刻相随",
        "午间愉快，愿身心自在轻松",
        "中午安好，愿工作一切顺利",
        "中午好，愿午后时光很惬意",
        "午安！愿你享受惬意中午",
        "中午时分，愿快乐常围绕你",
        "中午好，愿笑容时刻挂嘴边",
        "中午好，休息一下，放松心情！",
        "中午愉快，享受美好的午餐！",
        "中午好，午休时间，放松一下！",
        "中午好，保持元气，继续奋斗！",
        "中午好，午饭吃好，下午精神更好！",
        "中午好，享受美好的午餐时光！",
        "中午好，愿你的每一天都充满阳光！",
        "中午愉快，笑容可掬，心情美好！",
        "中午好，愿你的事业蒸蒸日上！"
    ]

    return list[random.randint(0, len(list) - 1)]


def get_goodnight_words():
    list = [
        "期待下午的阳光洒满心田。",
        "下午的时间，总是充满希望。",
        "盼望下午能有一个小小的休息。",
        "希望下午的时光如诗如画。",
        "下午，期待着美好的一切到来。",
        "下午的宁静，给了我满满的动力。",
        "期待下午有更多的美好发现。",
        "下午的阳光，洒进了我的心房。",
        "期待下午的时间更加充实。",
        "下午，是放松心情的时刻。"
        "期待下午的阳光洒满心田。",
        "下午的时间，总是充满希望。",
        "盼望下午能有一个小小的休息。",
        "希望下午的时光如诗如画。",
        "下午，期待着美好的一切到来。",
        "下午的宁静，给了我满满的动力。",
        "期待下午有更多的美好发现。",
        "下午的阳光，洒进了我的心房。",
        "期待下午的时间更加充实。",
        "下午，是放松心情的时刻。",
        "下午的风，吹动了我的心情。",
        "下午，感受每一缕温暖的阳光。",
        "下午的空气，格外清新。",
        "期待下午的每一个小惊喜。",
        "午后的光线洒满每个角落。",
        "下午的时光，适合放慢脚步。",
        "期待下午可以有一个小小的冒险。",
        "午后的闲暇，时间悄悄流逝。",
        "下午的世界，充满了安静与美好。",
        "下午的光景是一天中最温暖的时光。"
    ]

    return list[random.randint(0, len(list) - 1)]

# 获取当前时间
def get_weekday():
    weekd = ''
    # 日期时间
    date = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %X")
    # 农历日期
    now = str(datetime.now().strftime('%Y-%m-%d')).split("-")
    year, month, day = int(now[0]), int(now[1]), int(now[2])
    nongli_date = zhdate.ZhDate.from_datetime(datetime(year, month, day) + timedelta())
    # nongli_date = zhdate.ZhDate.from_datetime(datetime.now() + timedelta()) 老版代码不予使用
    # 星期fgv
    dayOfWeek = (datetime.now() + timedelta()).weekday()
    if dayOfWeek == 0:
        weekd = date + "  星期一\n" + str(nongli_date)
    if dayOfWeek == 1:
        weekd = date + "  星期二\n" + str(nongli_date)
    if dayOfWeek == 2:
        weekd = date + "  星期三\n" + str(nongli_date)
    if dayOfWeek == 3:
        weekd = date + "  星期四\n" + str(nongli_date)
    if dayOfWeek == 4:
        weekd = date + "  星期五\n" + str(nongli_date)
    if dayOfWeek == 5:
        weekd = date + "  星期六\n" + str(nongli_date)
    if dayOfWeek == 6:
        weekd = date + "  星期日\n" + str(nongli_date)
    return weekd


# 获取天气
def get_weather(city, api_key='7c75b7045984a1ffc81b7bf751b783c1'):
    weather = None
    temperature = None
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={api_key}"

    # 发送请求
    response = requests.get(url)

    # 检查响应是否成功
    if response.status_code == 200:
        data = response.json()

        # 判断API返回的状态
        if data['status'] == '1':  # 状态为1表示成功
            # 获取实况天气信息
            weather_info = data['lives'][0]  # 由于返回的lives是一个列表，我们取第一个元素
            weather = weather_info['weather']
            temperature = int(weather_info['temperature'])

    return weather, temperature


# 计算在一起的日期
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 计算距离下一次生日多少天
def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now() + timedelta():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 计算到元旦、春节的日期
def get_spr(yd, sp):
    next1 = datetime.strptime(str(date.today().year) + "-" + yd, "%Y-%m-%d")
    if next1 < datetime.now() + timedelta():
        next1 = next1.replace(year=next1.year + 1)
        j_yd = (next1 - today).days
    else:
        j_yd = (next1 - today).days

    next2 = datetime.strptime(str(date.today().year) + "-" + sp, "%Y-%m-%d")
    if next2 < datetime.now() + timedelta():
        next2 = next2.replace(year=next2.year + 1)
        j_cj = (next2 - today).days
    else:
        # 2023年2月10日解除注释
        # j_cj = (next2 - today).days

        # 2023年2月10日将下列代码注释掉
        next2 = next2.replace(year=next2.year + 1)
        j_cj = (next2 - today).days
    return j_yd, j_cj


# 每日金句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()

    # 获取返回的文本
    text = words.json()['data']['text']

    # 如果文本的长度大于20个字，重新请求
    if len(text) > 20:
        return get_words()

    return text


# 字体颜色，随机 每次不一样
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 电影
def top_mv():
    # 1 爬取源
    url = "https://movie.douban.com/chart"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36 "
    }

    # 2 发起http请求
    spond = requests.get(url, headers=header)
    res_text = spond.text
    # 3 内容解析
    soup = BeautifulSoup(res_text, "html.parser")
    soup1 = soup.find_all(width="75")  # 解析出电影名称
    # print(soup1[0]['alt'])
    soup2 = soup.find_all('span', class_="rating_nums")  # 解析出评分
    # print(soup2[0].text)
    # 4数据的处理

    """简单处理1，输入数值N，返回排第N的电影名及评分"""

    """处理2，将电影名和评分组成[{电影名：评分},{:}]的形式"""
    list_name = []  # 将电影名做成一个列表
    for i in range(10):
        list_name.append(soup1[i]['alt'])

    list_value = []  # 将评分值做成一个列表
    try:
        for i in range(10):
            list_value.append(soup2[i].text)
    except Exception as E:
        print(E)

    dict_name_value = dict(zip(list_name, list_value))  # 将两个list转化为字典dict

    mv_top = sorted(dict_name_value.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 字典排序,type==list

    show = ''
    for i in range(0, 1):
        mv_top_name = mv_top[i][0]  # 取出电影名,后期直接使用
        mv_top_value = mv_top[i][1]  # 取出评分，后期直接使用
        show = str(mv_top_name) + ":" + str(mv_top_value) + "分"

    return show


"""
3、调用函数，获取数据，保存为字典格式数据
"""
# 获取天气和温度
wea1, temperature1 = get_weather(city1)
wea2, temperature2 = get_weather(city2)

# 计算到春节的天数
j_yd, j_cj = get_spr("01-01", "02-17")
# 如果温度过高，提示语
sid = ""
if temperature1 >= 23:
    sid = "室外温度较高，注意喝水哦"
elif temperature1 <= 17:
    sid = "室外温度过低，记得多穿点衣服保暖"
else:
    sid = "温度不高不低，但也要注意及时补水哦"

# 提醒吃饭
now_time = (int(datetime.now().strftime("%H")) + 8) % 24  # 使用 % 24 确保小时在 0-23 范围内
eat = ""
m_n_a = ""
if 9 > now_time > 0:
    eat = get_morning_words()
    m_n_a = "早上好吖！"
if 12 > now_time >= 9:
    eat = get_eatmorning_words()
    m_n_a = "上午好吖！"
if 14 > now_time >= 12:
    eat = get_eatmorning_words()
    m_n_a = "中午好吖！"
if 18 > now_time >= 14:
    eat = get_goodnight_words()
    m_n_a = "下午好吖！"
if 24 >= now_time >= 18:
    eat = get_goodnight_words()
    m_n_a = "记得晚上早点睡觉哈，然后做个好梦！"

# 数据整理
data = {"m_n_a": {"value": m_n_a, "color": get_random_color()},
        "eat": {"value": eat, "color": get_random_color()},
        "city1": {"value": city1, "color": get_random_color()},
        "daytime": {"value": get_weekday(), "color": get_random_color()},
        "weather1": {"value": wea1, "color": get_random_color()},
        "temperature1": {"value": str(temperature1) + "℃", "color": get_random_color()},
        "sid": {"value": sid, "color": get_random_color()},
        "yd": {"value": j_yd, "color": get_random_color()},
        "cj": {"value": j_cj, "color": get_random_color()},
        "city2": {"value": city2, "color": get_random_color()},
        "weather2": {"value": wea2, "color": get_random_color()},
        "temperature2": {"value": str(temperature2) + "℃", "color": get_random_color()},
        "mv": {"value": top_mv(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
        }
# "love_days": {"value": get_count(), "color": get_random_color()},
# "birthday_lover": {"value": get_birthday(birthday_lover), "color": get_random_color()},
# "birthday_my": {"value": get_birthday(birthday_my), "color": get_random_color()},
"""
4、实例化微信客户端
"""
# 模拟登录微信客户端
client = WeChatClient(app_id, app_secret)
# 实例化微信客户端x
wm = WeChatMessage(client)

"""
5、发送消息
"""
# 参数 接收对象、消息模板ID、数据（消息模板里面的的变量与字典数据做匹配）
for i in range(0, len(user_id1)):
    res = wm.send_template(user_id1[i], template_id, data)
    # 打印消息发送情况
    print(res)
