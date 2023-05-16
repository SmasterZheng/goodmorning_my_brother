# from datetime import date, datetime
import datetime
import lunarcalendar
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

today = datetime.datetime.today()
start_date = os.environ['START_DATE']
birthday = os.environ['BIRTHDAY']
#微信平台的app_id
app_id = os.environ["APP_ID"]
#微信平台的app_secret
app_secret = os.environ["APP_SECRET"]
#天气平台的app_id
wea_appid = os.environ["WEA_APPID"]
#天气平台的app_secret
wea_appsecret = os.environ["WEA_APPSECRET"]
# 用户ID
user_id = os.environ["USER_ID"]
# 模板ID
template_id = os.environ["TEMPLATE_ID"]



def get_weather():
    """从易客云天气api中获取天气，不过免费的只有2000次调用机会"""

    # todo 后续加入 多个城市
    city1, city2, city3 = '南京', '上饶', '襄阳'
    url1 = f"https://v0.yiketianqi.com/api?unescape=1&version=v62&appid={wea_appid}&appsecret={wea_appsecret}&city={city1}"
    # url2 = f"https://v0.yiketianqi.com/api?unescape=1&version=v62&appid={wea_appid}&appsecret={wea_appsecret}&city={city2}"
    # url3 = f"https://v0.yiketianqi.com/api?unescape=1&version=v62&appid={wea_appid}&appsecret={wea_appsecret}&city={city3}"
    response = requests.get(url1)
    # 解析响应数据
    data = json.loads(response.text)
    wea = data['wea']  # 天气
    tem = data['tem']  # 当前气温
    min_max_tem = f"{data['tem2']}-{data['tem1']}"  # 今日温度范围
    return wea, tem, min_max_tem


def get_count():
    delta = today - datetime.datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    # 如果今年的生日已经过去了，那么下一个生日就是明年的
    if birthday_date < today.replace(year=today.year):
        next_birthday = birthday_date.replace(year=today.year + 1)
    else:
        next_birthday = birthday_date.replace(year=today.year)

    # 计算天数差
    days_left = (next_birthday - today).days
    return days_left


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
      return '虽然没有太多甜言蜜语，但记住我爱你！'
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def main():
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    wea, temperature, tem = get_weather()
    data = {"weather":{"value":wea},"temperature":{"value":temperature},"min_max_tem":{"value":tem},"love_day":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
    res = wm.send_template(user_id, template_id, data)
    print(res)


if __name__ == '__main__':
    main()