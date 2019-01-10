#!/usr/bin/env python
# export PATH=$PATH:/home/muru/myFlaskPython
from selenium import webdriver
import time
import lxml
import json
from bs4 import BeautifulSoup
import unicodedata
from matplotlib.cbook import flatten


def get():

    url = "https://www3.nhk.or.jp/news/easy/"
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(options=opt)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    #用來判斷漢字 與漢字片假名使用
    isJp =0
    #標題字串分隔儲存
    titleStr=""
    #內容字串分割儲存
    bodyStr=""





    title = []
    url = []
    time = []
    img = []
    newsJson = []

    #遍歷HTML 先將 class top-news-list找出來
    for post in soup.find_all('section', "top-news-list"):
        # print("post==========",post)
        ##找到title的class 開始遍歷  <div class=top-news-list__pickup news-list-item"
        for titleItem in post.find_all("div", "top-news-list__pickup news-list-item"):
            #標題圖片 <figure class=news-list-item__image"
            for titleImg in titleItem.find_all('figure', "news-list-item__image"):
                '''
                用.img來去找 <a裡面的 img  然後在使用 img[src] 去src 找出資料
                 <a href="./k10011771031000/k10011771031000.html">
	                <img alt="" onerror="this.src='./images/noimg_default_easy.png';"
	                src="https://www3.nhk.or.jp/news/html/20190108/../20190108/K10011771031_1901081458_1901081502_01_02.jpg"/>
	             </a>
                '''
                if titleImg.img:
                    print("標題圖片==", titleImg.img['src'])
                    img.append(titleImg.img['src'])


            #標題內容
            for name in titleItem.find_all('em', "title"):
                print("標題內容==", name)
            # print("內容標題==", bodyTtile)
            # 剛開始遍歷先將字串清空
            titleStr = ""
            # 將字串分割
            for string in name.strings:
                # 判斷是不是漢字
                if is_japanese(string):
                    # 是漢字的話漢字後面加上&
                    titleStr += string + "&"
                    isJp = 1
                else:
                    # 如果上一筆是漢字isJp=1  結束要加上空白
                    if isJp == 1:
                        isJp = 0
                        titleStr += string + " "
                    # 如果isJp=0 代表前面沒漢字　不需要加空白　不=0的話 代表前面有漢字 將is存成2
                    else:
                        titleStr += string + " "
            # 標題內容時間
            for titleTime in titleItem.find_all('time', "time"):
                #.string 這樣可以只找出裡面的字串
                if titleTime.string:
                    time.append(titleTime.string)
                    print("標題時間==", titleTime.string)

            #得到<a裡面href 標題頁面的URL
            for titleUrl in titleItem.find_all('a', href=True):
                if titleUrl.text:
                    url.append(titleUrl['href'])
                    print("標題url==", titleUrl['href'])

        title.append(titleStr)

        # json_string = json.dumps([ob.__dict__ for ob in titlejson])
        #內容
        for body in post.find_all("ul", "top-news-list__items news-list-grid"):

            # print("body==========", body)
            #得到內容 時間 4個 item
            for bodyItem in body.find_all('h1', "news-list-item__title"):
                # print("bodyItem========", bodyItem)
                #將em class 字串 排除 然後只抓取日文 分割遍歷 例如這種內容→ <em class="title"><ruby>住<rt>す</rt></ruby>んでいる<ruby>人<rt>ひと</rt></ruby>
                for bodyTtile in bodyItem.find_all('em', "title"):
                    # print("內容標題==", bodyTtile)
                    #剛開始遍歷先將字串清空
                    bodyStr=""
                    #將字串分割
                    for string in bodyTtile.strings:
                        #判斷是不是漢字
                        if is_japanese(string):
                            #是漢字的話漢字後面加上&
                            bodyStr += string+"&"
                            isJp=1
                        else:
                            #如果上一筆是漢字isJp=1  結束要加上空白
                            if isJp==1:
                                isJp=0
                                bodyStr+= string+" "
                            #如果isJp=0 代表前面沒漢字　不需要加空白　不=0的話 代表前面有漢字 將is存成2
                            else:
                                bodyStr += string + " "
                    #如果只要<ruby> 可以使用這樣
                    # if bodyTtile.ruby:

                title.append(bodyStr)
                #時間
                for bodyTime in bodyItem.find_all('time', "time"):
                    if bodyTime.string:
                        time.append(bodyTime.string)
                        print("內容時間==", bodyTime.string)
                #URL
                for bodyUrl in bodyItem.find_all('a', href=True):
                    if bodyUrl.text:
                        url.append(bodyUrl['href'])
                        print("內容URL==", bodyUrl['href'])

            for bodyImg in body.find_all('figure', "news-list-item__image"):
                # print(bodyImg)
                if bodyImg.img:
                    img.append(bodyImg.img['src'])
                    print("內容圖片==", bodyImg.img['src'])


            # print(newsJson)
            # newsJson += list(flatten(zip(title, img, time, url)))

    for a, b, c, d in zip(title, img, time, url):
        result = {}
        result['title'] = a
        result['img'] = b
        result['time'] = c
        result['url'] = d
        newsJson.append(result)
    print(json.dumps(newsJson))


    driver.close()
    return "ok"

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name:
            return True
        return False


    return 'ok'

