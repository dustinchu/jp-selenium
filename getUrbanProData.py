#!/usr/bin/env python
# export PATH=$PATH:/home/muru/myFlaskPython
from pyvirtualdisplay import Display
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import unicodedata



def test():
    url = "https://asheville.craigslist.org/search/fua"
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(options=opt)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    i =0
    for post in soup.find_all('li', "result-row"):
        i+=1
        print(post ,"第=====", i, "次")
        for post_content in post.find_all("a", "result-image gallery"):
            print(post, "aaaaaaaaaaaaaaaaaa=====", i, "次")
            print(post_content['href'])
            for pic in post_content.find_all("img"):
                print(pic['src'])
    return "testok"


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

            #標題內容
            for title in titleItem.find_all('em', "title"):
                print("標題內容==", title)
            # print("內容標題==", bodyTtile)
            # 剛開始遍歷先將字串清空
            titleStr = ""
            # 將字串分割
            for string in title.strings:
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
                    print("標題時間==", titleTime.string)

            #得到<a裡面href 標題頁面的URL
            for titleUrl in titleItem.find_all('a', href=True):
                if titleUrl.text:
                    print("標題url==", titleUrl['href'])
        print(titleStr)
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
                print(bodyStr)
                #時間
                for bodyTime in bodyItem.find_all('time', "time"):
                    if bodyTime.string:
                        print("內容時間==", bodyTime.string)
                #URL
                for bodyUrl in bodyItem.find_all('a', href=True):
                    if bodyUrl.text:
                        print("內容URL==", bodyUrl['href'])

            for bodyImg in body.find_all('figure', "news-list-item__image"):
                # print(bodyImg)
                if bodyImg.img:
                    print("內容圖片==", bodyImg.img['src'])


    driver.close()
    return "ok"

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name :
            return True
        return False



html_doc ="""
<!DOCTYPE html><!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7 eq-ie6"><![endif]--><!--[if IE 7]><html class="no-js lt-ie9 lt-ie8 eq-ie7"> <![endif]--><!--[if IE 8]><html class="no-js lt-ie9 eq-ie8"> <![endif]--><!--[if gt IE 8]><!--><html xmlns="http://www.w3.org/1999/xhtml" class="no-js" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;"><!--<![endif]--><head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# website: http://ogp.me/ns/website#">
<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta http-equiv="X-UA-Compatible" content="requiresActiveX=true" />

<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="description" content="NEWS WEB EASY?、小?生?中?生?皆???、日本?住????外?人??????、?????????　??????伝??????????。" />
<meta name="keywords" content="ＮＨＫ,????,ＮＨＫ????,NHK NEWS WEB,子??,????,???,小?生,中?生,Japanese,learn,lesson" />
<title>NEWS WEB EASY</title>

<meta property="og:site_name" content="NEWS WEB EASY" />
<meta property="og:title" content="NEWS WEB EASY" />
<meta property="og:locale" content="ja_JP" />
<meta property="og:description" content="NEWS WEB EASY?、小?生?中?生?皆???、日本?住????外?人??????、?????????　??????伝??????????。" />
<meta property="og:url" content="https://www3.nhk.or.jp/news/easy/" />
<meta property="og:image" content="https://www3.nhk.or.jp/news/easy/images/og-image.png" />
<meta property="og:type" content="website" />

<link rel="shortcut icon" type="image/x-icon" href="//www.nhk.or.jp/favicon.ico" />
<link rel="canonical" href="https://www3.nhk.or.jp/news/easy/" />
<script type="application/ld+json">{"@context":"http://schema.org","@type":"Organization","name":"NHK?????","url":"https://www.nhk.or.jp/","logo":"https://www.nhk.or.jp/nhk-600x600.png"}</script><script type="text/javascript" async="" src="//www.nhk.or.jp/common/tc/am.js"></script><script src="https://assets.adobedtm.com/launch-EN7d55f9d4f78b412597c9c6586b2a86ec.min.js" type="text/javascript" charset="utf-8" async=""></script><script src="/common/js/nol_tools.js"></script>

<link rel="stylesheet" href="./css/style-v2.css" />
<script src="https://www3.nhk.or.jp/common/jquery/jquery-2.2.js"></script>
<script src="https://www3.nhk.or.jp/common/sp/nol_SmartPhone.js" charset="utf-8"></script><script type="text/javascript" src="//www.nhk.or.jp/common/tc/a.js" charset="utf-8"></script>
<script src="https://www3.nhk.or.jp/common/sns/nol_share.js" charset="UTF-8"></script>
<script src="https://www3.nhk.or.jp/news/r/js/exist.js" charset="UTF-8"></script>
<script>NHKSNS.initSNSOnLoad();</script>
<script type="text/javascript">var _sf_startpt = (new Date()).getTime();var _cb_sections_preset = 'EASY';</script>
<style type="text/css">@charset "utf-8";div#nol_header.pattern1 #pattern2-logo{display:none}#nol_header.pattern1 .nol_menuBtn_common&gt;li:hover,#nol_header.pattern1 .nol_menuBtn_common&gt;li.nol_menuBtn_click{background:#333}#nol_header.pattern1 .nol_menuBtn_common&gt;li:hover *,#nol_header.pattern1 .nol_menuBtn_common&gt;li.nol_menuBtn_click *{color:#fff}#nol_header.pattern1 .nol_menuBtn_common&gt;li:hover a *,#nol_header.pattern1 .nol_menuBtn_common&gt;li.nol_menuBtn_click a *{color:#fff}#nol_header #nol_headerGroup02 .nol_menuBtn_common&gt;li:hover,#nol_header #nol_headerGroup02 .nol_menuBtn_common&gt;li.nol_menuBtn_click{background:none}#nol_header.pattern1 #nol_searchArea.nol_menuBtn_common&gt;li:hover,#nol_header.pattern1 #nol_searchArea.nol_menuBtn_common&gt;li.nol_menuBtn_click{background:none}#nol_header.pattern1 #nol_searchArea #nol_menuSearch_input input.nol_btSearch{background:url(//www.nhk.or.jp/common/res/img2/icon_input_black.png) no-repeat left top}#nol_header.pattern1 li span.nol_item_inner{border-right:solid 1px #7f7f7f}#nol_header.pattern1 li.nol_item7 span.nol_item_inner{border-right:none}#nol_header.pattern1 li.nol_item_first span.nol_item_inner{border-left:solid 1px #7f7f7f}div#nol_header.pattern1 #nol_headerGroup02 #nol_menuNav&gt;li.nol_menuBtn_hover span.nol_item_inner{padding:0 10px}div#nol_header.pattern1 #nol_headerGroup02 #nol_menuNav&gt;li.nol_item7 span.nol_item_inner{border-right:none}div#nol_header.pattern1 #nol_headerGroup02 #nol_menuNav&gt;li.nol_item_first.nol_menuBtn_hover span.nol_item_inner{border-left:solid 1px #7f7f7f;border-right:solid 1px #7f7f7f}#nol_header.pattern1 div.nol_modalWindow{background:rgba(51,51,51,.95)}#nol_header.pattern1 div.nol_modalWindow *{color:#fff}#nol_header.pattern1 #nol_searchArea .nol_item8{border:solid 1px #7f7f7f}#nol_header.pattern1 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li{border-right:solid 1px #7f7f7f}#nol_header.pattern1 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner:hover{background:#5482b1}#nol_header.pattern1 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner span.nol_navList_hd{background:url(//www.nhk.or.jp/common/res/img2/icon_navhd_white.png) no-repeat 10px 12px}#nol_header.pattern1 div#nol_prefSetting #nol_prefSetting_select02{background:#666}#nol_header.pattern1 .nol_modalWindow p.nol_close{background:url(//www.nhk.or.jp/common/res/img2/bg_close.png) no-repeat left top}#nol_header.pattern1 .nol_modalWindow p.nol_close:hover{background-position:left bottom}#nol_header.pattern1 #nol_searchArea #nol_menuSearch_input input.nol_wordInputArea{background:#999}#nol_header.pattern1 #nol_searchArea #nol_menuSearch_input input.nol_wordInputArea *{color:#666}#nol_header.pattern1 #nol_WindowMore #nol_subGlobal{border:solid 1px #4c4c4c}#nol_header.pattern1 #nol_WindowMore #nol_subGlobal li *{color:#b2b2b2}#nol_header.pattern1 #nol_WindowMore #nol_subGlobal li.nol_menuBtn_sub{cursor:pointer}#nol_header.pattern1 #nol_WindowMore #nol_subGlobal li.nol_active{background:#666}#nol_header.pattern1 #nol_WindowMore #nol_subGlobal li.nol_active *{color:#fff}#nol_header.pattern1 .nol_modalWindow_more{background:#333}#nol_header.pattern1 .nol_modalWindow_more *{color:#fff}div#nol_header.pattern2 #pattern1-logo{display:none}#nol_header.pattern2{background:#fff;color:#999}#nol_header div.nol_inner span.nol_logo_linkBox{background:#333}#nol_header.pattern2 .nol_menuBtn_common&gt;li:hover,#nol_header.pattern2 .nol_menuBtn_common&gt;li.nol_menuBtn_click{background:#e6e6e6}#nol_header.pattern2 .nol_menuBtn_common&gt;li:hover *,#nol_header.pattern2 .nol_menuBtn_common&gt;li.nol_menuBtn_click *{color:#333}#nol_header.pattern2 .nol_menuBtn_common&gt;li:hover a,#nol_header.pattern2 .nol_menuBtn_common&gt;li.nol_menuBtn_click a{color:#333}#nol_header.pattern2 .nol_menuBtn_common&gt;li:hover a *,#nol_header.pattern2 .nol_menuBtn_common&gt;li.nol_menuBtn_click a *{color:#333}#nol_header #nol_headerGroup02 .nol_menuBtn_common&gt;li:hover,#nol_header #nol_headerGroup02 .nol_menuBtn_common&gt;li.nol_menuBtn_click{background:none}#nol_header.pattern2 #nol_searchArea.nol_menuBtn_common&gt;li:hover,#nol_header.pattern2 #nol_searchArea.nol_menuBtn_common&gt;li.nol_menuBtn_click{background:none}#nol_header.pattern2 #nol_searchArea #nol_menuSearch_input input.nol_btSearch{background:url(//www.nhk.or.jp/common/res/img2/icon_input_white.png) no-repeat left top}#nol_header.pattern2 li span.nol_item_inner{border-right:solid 1px #f2f2f2;padding:0 10px}#nol_header.pattern2 li.nol_item7 span.nol_item_inner{border-right:none}#nol_header.pattern2 li.nol_item_first span.nol_item_inner{border-left:solid 1px #f2f2f2}div#nol_header.pattern2 #nol_headerGroup02 #nol_menuNav&gt;li.nol_menuBtn_hover span.nol_item_inner{padding:0 10px}div#nol_header.pattern2 #nol_headerGroup02 #nol_menuNav&gt;li.nol_item7 span.nol_item_inner{border-right:none}div#nol_header.pattern2 #nol_headerGroup02 #nol_menuNav&gt;li.nol_item_first.nol_menuBtn_hover span.nol_item_inner{border-left:solid 1px #f2f2f2;border-right:solid 1px #f2f2f2}div#nol_header.pattern2 #nol_headerGroup02 #nol_menuNav&gt;li.nol_menuBtn_hover span.nol_item_inner{padding:0 10px}#nol_header.pattern2 div.nol_modalWindow{background:rgba(231,231,231,.95);color:#333}#nol_header.pattern2 div.nol_modalWindow a *{color:#333}#nol_header.pattern2 #nol_searchArea .nol_item8{border:solid 1px #e6e6e6}#nol_header.pattern2 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li{border-right:solid 1px #ccc}#nol_header.pattern2 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner:hover{background:#a5c2e0}#nol_header.pattern2 .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner span.nol_navList_hd{background:url(//www.nhk.or.jp/common/res/img2/icon_navhd_black.png) no-repeat 10px 12px}#nol_header.pattern2 div#nol_prefSetting #nol_prefSetting_select02{background:#cecece}#nol_header.pattern2 .nol_modalWindow p.nol_close{background:url(//www.nhk.or.jp/common/res/img2/bg_close.png) no-repeat right top}#nol_header.pattern2 .nol_modalWindow p.nol_close:hover{background-position:right bottom}#nol_header.pattern2 #nol_searchArea #nol_menuSearch_input input.nol_wordInputArea{background:#f2f2f2;border:solid 1px #f2f2f2;color:#b2b2b2;height:20px}#nol_header.pattern2 #nol_searchArea #nol_menuSearch_input.nol_hover input.nol_wordInputArea,#nol_header.pattern2 #nol_searchArea #nol_menuSearch_input.nol_focus input.nol_wordInputArea{border:solid 1px #999}#nol_header.pattern2 #nol_WindowMore #nol_subGlobal{border:solid 1px #ccc}#nol_header.pattern2 #nol_WindowMore #nol_subGlobal li *{color:#666}#nol_header.pattern2 #nol_WindowMore #nol_subGlobal li.nol_active{background:#fff}#nol_header.pattern2 #nol_WindowMore #nol_subGlobal li.nol_active *{color:#333}#nol_header.pattern2 .nol_modalWindow_more{background:#e7e7e7}#nol_header.pattern2 .nol_modalWindow_more *{color:#333}div#nol_header #pattern1-logo,div#nol_header #pattern2-logo{width:55px!important}div#nol_footer div.nol_table div p.nol_footerLogo img{width:68px!important}div#nol_header img{-ms-interpolation-mode:bicubic}div#nol_footer img{-ms-interpolation-mode:bicubic}body{margin:0}div#nol_header{background:#666;width:100%;min-width:768px;z-index:500;font-family:"????角? Pro W3","????",Meiryo,"ＭＳ Ｐ????",sans-serif,Lucida Grande,Hiragino Kaku Gothic Pro,MS PGothic,Arial,Verdana}div#nol_header a{text-decoration:none;color:#ccc}div#nol_header a:hover{text-decoration:none}div#nol_header li{list-style:none}div#nol_header *,div#nol_contentsFooter *{margin:0;padding:0;font-size:12px;line-height:1;-webkit-box-sizing:content-box;-ms-box-sizing:content-box;box-sizing:content-box}div#nol_contentsFooter a{text-decoration:none;color:#666}div#nol_contentsFooter a:hover{opacity:.7}div#nol_header img,div#nol_contentsFooter img{border:none}div.nol_inner{position:relative;text-align:left;margin:0 auto}#nol_header.pattern1 *{color:#ccc}#nol_header.pattern2 *{color:#999}#nol_contentsFooter *{color:#666}div#nol_header div.nol_inner{min-height:30px;margin:auto;position:relative;background:#666}#nol_header div.nol_inner span.nol_logo_linkBox{background:#333;display:block;text-indent:0;position:relative}#nol_header div.nol_inner span.nol_logo_linkBox:hover{background:rgba(51,51,51,.95)}#nol_header div.nol_inner span.nol_linkIcon{display:block;position:absolute;left:32px;top:-5px}#nol_header div.nol_inner span.nol_linkIcon img{vertical-align:top}div#nol_header div.nol_inner p.nol_logo{float:left;margin:8px 18px 0 0;cursor:pointer}div#nol_header div.nol_inner span.nol_logo_linkBox{display:none;position:absolute;left:0;bottom:-40px;text-align:center}div#nol_header div.nol_inner span.nol_logo_linkBox a{line-height:40px;height:40px;padding:0 10px;font-size:12px;display:block;color:#fff}div#nol_header div.nol_inner p#nol_headerLogo2{float:left;width:149px;height:40px}div#nol_header div.nol_inner p#nol_headerLogo2 img{margin:5px 10px 0 0}div#nol_header{min-height:1%;position:relative;color:#ccc}div#nol_header:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_header div.nol_inner{padding:0 10px}div#nol_header #nol_headerGroup01{float:left}div#nol_header li span.nol_item_inner{padding:0 10px}div#nol_header li.nol_menuBtn_hover span.nol_item_inner{border:none;padding-right:11px}div#nol_header li.nol_menuBtn_hover.nol_item_first span.nol_item_inner{border:none;padding-left:11px}div#nol_header #nol_headerGroup01 #nol_menuGlobal:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_header #nol_headerGroup01 #nol_menuGlobal&gt;li{float:left;cursor:pointer}div#nol_header #nol_headerGroup01 #nol_menuGlobal&gt;li span.nol_item_wrap{display:block;padding:9px 0}div#nol_header #nol_headerGroup01 #nol_menuGlobal li.nol_itemMore{display:none}div#nol_header #nol_headerGroup02{float:right}div#nol_header #nol_headerGroup02 #nol_menuNav:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_header #nol_headerGroup02 #nol_menuNav&gt;li{float:left;cursor:pointer;padding:9px 0}div#nol_header #nol_searchArea{float:right;padding-top:4px}div#nol_header #nol_searchArea:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_header #nol_searchArea&gt;li{float:left;cursor:pointer}div#nol_header #nol_searchArea .nol_item8{width:92px;margin-right:5px;margin-top:1px;border:solid 1px #7f7f7f;position:relative}div#nol_header #nol_searchArea .nol_item8 .nol_item_wrap{padding:3px 0 3px 5px}div#nol_header #nol_searchArea #nol_menuSearch_select .nol_item_wrap:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_header #nol_searchArea #nol_menuSearch_select .nol_item_wrap&gt;p{float:left}div#nol_header #nol_searchArea #nol_menuSearch_select #nol_pref_hd{margin-right:3px}div#nol_header #nol_searchArea #nol_menuSearch_select #nol_pref_config{position:absolute;right:3px;top:7px;height:4px}div#nol_header #nol_searchArea #nol_menuSearch_select #nol_pref_config img{vertical-align:top}div#nol_header #nol_searchArea #nol_menuSearch_input input{vertical-align:top}div#nol_header #nol_searchArea #nol_menuSearch_input input.nol_wordInputArea{border:none;height:22px;width:142px;vertical-align:super;font-size:12px;line-height:22px;margin:0;padding-left:6px}#nol_header #nol_searchArea #nol_menuSearch_input.nol_hover input.nol_wordInputArea,#nol_header #nol_searchArea #nol_menuSearch_input.nol_focus input.nol_wordInputArea{background:#fff;color:#000}#nol_header #nol_searchArea #nol_menuSearch_input input.nol_btSearch{width:32px;height:22px;border:none}#nol_header #nol_searchArea #nol_menuSearch_input.nol_hover input.nol_btSearch,#nol_header #nol_searchArea #nol_menuSearch_input.nol_focus input.nol_btSearch{background-image:url(//www.nhk.or.jp/common/res/img2/icon_input_focus.png)}div#nol_header div.nol_modalWindow{position:absolute;top:30px;text-align:left;z-index:150;display:none}#nol_header li.nol_menuBtn_hover div.nol_modalWindow{display:block;opacity:1;animation-duration:.3s;animation-name:fade-in;-moz-animation-duration:.3s;-moz-animation-name:fade-in;-webkit-animation-duration:.3s;-webkit-animation-name:fade-in}#nol_header li.nol_menuBtn_click div.nol_modalWindow{display:block}@keyframes fade-in{0%{display:none;opacity:0}1%{display:block;opacity:0}100%{display:block;opacity:1}}@-webkit-keyframes fade-in{0%{display:none;opacity:0}1%{display:block;opacity:0}100%{display:block;opacity:1}}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList{width:737px}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList:after{content:".";display:block;height:0;clear:both;visibility:hidden}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li{float:left;width:235px;margin:5px 0;border-right:solid 1px #7f7f7f;padding:0 5px}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li:nth-child(3n){border-right:none}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner{height:60px;border-radius:3px}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner a{display:block;height:50px}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner span{display:block}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner span.nol_navList_hd{padding:10px 0 0 20px;font-size:14px}#nol_header .nol_modalWindow div.nol_navList_wrap ul.nol_navList li div.nol_navList_inner span.nol_navList_sub{padding:10px 0 0 20px}div#nol_header div.nol_modalWindowInner p.nol_text{line-height:1.4}div#nol_header .nol_modalWindow p.nol_close{position:absolute;bottom:-35px;right:0;margin:0;cursor:pointer;width:35px;height:35px;text-indent:-9999px;line-height:0}#nol_header #nol_WindowMore{padding:15px 0;text-align:center;left:30px;width:737px}#nol_header #nol_WindowMore #nol_subGlobal{text-align:center;padding:2px;border-radius:5px;display:inline-block}#nol_header #nol_WindowMore #nol_subGlobal li{display:inline-block;padding:5px 15px;border-radius:5px}#nol_header #nol_WindowMore .nol_modalWindow_more{display:none;text-align:left}#nol_header #nol_WindowMore .nol_modalWindow_more.nol_show{display:block}div#nol_header #nol_Window01.nol_modalWindow{left:83px}div#nol_header #nol_Window02.nol_modalWindow{left:189px}div#nol_header #nol_Window03.nol_modalWindow{left:258px}div#nol_header #nol_Window04.nol_modalWindow{left:327px}div#nol_header #nol_Window05.nol_modalWindow{left:420px}div#nol_header #nol_Window06.nol_modalWindow{left:513px}div#nol_prefSetting{width:460px;padding:5px}#nol_header #nol_prefSetting.nol_modalWindow{right:0;top:25px}#nol_header #nol_prefSetting.nol_modalWindow.nol_modalWindow_hover{display:block}#nol_header #nol_prefSetting.nol_modalWindow.nol_modalWindow_click{display:block}div#nol_prefSetting #nol_nowSetting{text-align:center;margin-bottom:10px;padding-top:25px}div#nol_prefSetting #nol_nowSetting strong,div#nol_prefSetting #nol_nowSetting span{font-size:14px}div#nol_prefSetting select{vertical-align:middle;width:98px}div#nol_prefSetting select,div#nol_prefSetting option,div#nol_prefSetting input{color:#333!important}div#nol_prefSetting #nol_prefSetting_select01{padding:10px 15px 22px}div#nol_prefSetting #nol_prefSetting_select01 select{text-align:left}div#nol_prefSetting #nol_prefSetting_select01 input{vertical-align:middle}div#nol_prefSetting #nol_prefSetting_select01 .nol_prefSettingArea{text-align:center}div#nol_prefSetting #nol_prefSetting_select01 .nol_prefSettingArea p{display:inline-block;vertical-align:middle}div#nol_prefSetting #nol_prefSetting_select01 .nol_prefSettingArea #nol_prefList1_tag{margin-right:20px}div#nol_prefSetting #nol_prefSetting_select02{padding:20px 15px 6px;position:relative}div#nol_prefSetting #nol_prefSetting_select02:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_prefSetting #nol_prefSetting_select02 p.nol_text{float:left}div#nol_prefSetting #nol_prefSetting_select02 .nol_prefSettingArea{margin-left:126px}div#nol_prefSetting #nol_prefSetting_select02 .nol_prefSettingArea p{margin-bottom:10px;vertical-align:middle}div#nol_prefSetting #nol_prefSetting_select02 .nol_prefSettingArea select{margin-left:6px;vertical-align:middle}div#nol_prefSetting #nol_prefSetting_select02 .nol_prefSettingArea input{vertical-align:middle}div#nol_prefSetting #nol_prefSetting_select02 #nol_prefSetting_submit{position:absolute;right:25px;top:35px}div#nol_prefSetting select#nol_prefList1{margin:0}div#nol_prefSetting #nol_prefSetting_all,div#nol_prefSetting #nol_prefSetting_submit{cursor:pointer}#nol_header #nol_emergencyNews{padding:12px 10px;margin:0;background:#fff}#nol_header #nol_emergencyNews .nol_emergencyNews_inner{height:28px;max-width:862px;margin:0 auto;border:2px solid #c00}#nol_header #nol_emergencyNews .nol_emergencyNews_inner:after{content:".";display:block;height:0;clear:both;visibility:hidden}#nol_header #nol_emergencyNews .nol_emergencyNews_hd{float:left;width:9em;text-align:center;-webkit-box-sizing:border-box;box-sizing:border-box;background:#c00;color:#fff;font-size:15px;font-weight:400;height:100%;line-height:1.4em;padding:4px 0}#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox{padding:0 12px;border-left:2px solid #c00;margin-left:9em;height:100%;font-size:15px;line-height:28px}#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox p{top:0;white-space:nowrap;position:absolute;color:#c00;font-size:15px}#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox a,#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox span{color:#c00;font-size:15px}#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox a:hover{text-decoration:underline}#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox .tickbox,#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox #sokuhop,#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox span,#nol_header #nol_emergencyNews .nol_emergencyNews_txtBox a{height:100%!important;line-height:28px}#nol_contentsFooter{font-family:"????角? Pro W3","????",Meiryo,"ＭＳ Ｐ????",sans-serif,Lucida Grande,Hiragino Kaku Gothic Pro,MS PGothic,Arial,Verdana}#nol_contentsFooter p,#nol_contentsFooter img,#nol_contentsFooter ul,#nol_contentsFooter div{margin:0;padding:0}#nol_contentsFooter li{list-style:none;margin:0;padding:0}#nol_contentsFooter #nol_broadcastList{background:#ccc;color:#666;padding:0 60px;min-width:768px}#nol_contentsFooter #nol_broadcastList div.nol_broadcastList_inner{max-width:1100px;margin:0 auto}#nol_contentsFooter #nol_broadcastList p,#nol_contentsFooter #nol_broadcastList a,#nol_contentsFooter #nol_broadcastList li{font-size:14px}#nol_contentsFooter #nol_broadcastList p.nol_broadcastList_hd{padding:15px;background:url(//www.nhk.or.jp/common/res/img2/icon_foot_hd.png) no-repeat 2px 16px}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu&gt;li{border-top:dotted 1px #b3b3b3;padding:12px 0}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu&gt;li.nol_broadcastMenu_top{border-top:solid 1px #b3b3b3}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu&gt;li:after{content:".";display:block;height:0;clear:both;visibility:hidden}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu&gt;li p.nol_broadcastMenu_hd{width:174px;float:left;font-weight:700}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu ul.nol_broadcastMenu_sub{padding-left:174px}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu ul.nol_broadcastMenu_sub:after{content:".";display:block;height:0;clear:both;visibility:hidden}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu ul.nol_broadcastMenu_sub&gt;li{float:left;padding:0 8px;margin-bottom:6px;font-size:12px;border-right:solid 1px #b3b3b3}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu ul.nol_broadcastMenu_sub&gt;li.nol_broadcastMenu_sub_last{border-right:none}#nol_contentsFooter #nol_broadcastList ul.nol_broadcastMenu ul.nol_broadcastMenu_sub li a{font-size:12px}#nol_contentsFooter #nol_smInfo{background:#666;padding:20px 20px 0}#nol_contentsFooter #nol_smInfo a{display:block;max-width:1020px;min-width:728px;margin:0 auto;background:#999;padding:30px 0;text-align:center;font-size:40px;color:#fff}div#nol_footer div.nol_table{text-align:left;margin:0 auto}div#nol_footer div.nol_table div{vertical-align:middle}div#nol_footer div.nol_table div p.nol_footerLogo{width:68px;float:left;margin-right:10px}div#nol_footer div.nol_table div p.nol_copyright{padding:0 0 0 75px}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy{display:block;padding:0;line-height:1}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy img{width:310px}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy img#nol_copyB{display:none}div#nol_footer div.nol_table div p.nol_copyright span a{color:#000;padding:0 5px 0 0;font-size:12px;text-decoration:underline}div#nol_footer div.nol_table div ul.nol_link{padding:6px 10px 0 0;margin:0;font-size:14px}div#nol_footer div.nol_table div ul.nol_link:after{content:".";display:block;height:0;clear:both;visibility:hidden}div#nol_footer div.nol_table div ul.nol_link li{float:left;padding:0 10px;border-right:solid 1px #b3b3b3}div#nol_footer div.nol_table div ul.nol_link li:last-child{border-right:none;padding-right:0}div#nol_footer div.nol_table div ul.nol_link a{font-size:12px;color:#333;text-decoration:none}div#nol_footer div.nol_table div ul.nol_link a:hover{text-decoration:underline}div#nol_footer{padding:8px 10px}div#nol_footer{background:#666}div#nol_footer div.nol_table div ul.nol_link,div#nol_footer div.nol_table div ul.nol_link a{color:#ccc}div#nol_header div.nol_inner{width:auto;margin:auto}div#nol_footer div#nol_footerInner{width:auto;margin:0 auto}div#nol_footer div.nol_table{text-align:left;margin:0 auto;width:100%;display:table}div#nol_footer div.nol_table&gt;div{display:table-cell}div#nol_footer div.nol_table div.nol_copy_wrap{width:395px}div#nol_footer div.nol_table div p.nol_footerLogo{width:68px}div#nol_footer div.nol_table div p.nol_copyright{padding:0}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy{display:block;padding:0;line-height:1}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy img{width:310px}div#nol_footer div.nol_table div p.nol_copyright span.nol_copy img#nol_copyB{display:none}div#nol_footer div.nol_table div p.nol_copyright span a{color:#000;padding:0 5px 0 0;font-size:12px;text-decoration:underline}div#nol_footer div.nol_table div ul.nol_link{padding:8px 10px 0;margin:0;font-size:14px;float:right}div#nol_footer div.nol_table div ul.nol_link a{font-size:12px;text-decoration:none}#nol_footer.w1200 div.nol_table div ul.nol_link li{float:none;margin-bottom:10px;text-align:right;border:none;padding:0}#nol_footer.w720 div.nol_table&gt;div{display:block}#nol_footer.w720 div.nol_table div.nol_copy_wrap{width:auto;text-align:center}#nol_footer.w720 div.nol_table div.nol_copy_wrap p{display:inline-block}#nol_footer.w720 div.nol_table div p.nol_footerLogo{float:none}#nol_footer.w720 div.nol_table div ul.nol_link{float:none}#nol_footer.w720 div.nol_table div ul.nol_link li{text-align:center}#nol_loadcomplete{height:1px;</style><meta name="viewport" content="width=987" /><style>.nhk-snsbtn { margin-bottom: 15px; } ul.nhksns { list-style:none; display: inline; padding-left: 0; } ul.nhksns &gt; li { display: inline-block; vertical-align: middle; margin: 0.2em; } .nhksns-icon-s img { width:24px; } .nhksns-icon-m img { width: 32px; } .nhksns-icon-l img { width:40px; } .nhksns-help img { margin-left:6px; width: 18px; border: 1px solid #999; vertical-align: middle; }  img { border: none; } .nhksns-guide { vertical-align:middle; margin: 0 0 6px 0; font-weight: bold; } .nhksns img { border: none; }</style></head>
<body id="body" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;">
<aside id="nhkheader" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;">
  <script>
      nol_showCmnHeader({
          design: 'gray'
      });
  </script><div id="nolCmnHeaderSection" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;"><div id="nol_header" class="pattern1">
	<div class="nol_inner">
		<p class="nol_logo"><a href="https://www.nhk.or.jp/" onclick="nol_com.noltc('NOL_Header_NhkLogo');"><img id="pattern1-logo" src="//www.nhk.or.jp/common/res/img2/logo_header_black.png" alt="NHK" /></a><span class="nol_logo_linkBox"><a href="https://www.nhk.or.jp/" onclick="nol_com.noltc('NOL_Header_NhkLogo');">NHK????? ????</a><span class="nol_linkIcon"><img src="//www.nhk.or.jp/common/res/img2/icon_totop.png" alt="" style="width: auto;" /></span></span></p>
		<div id="nol_headerGroup01">
			<ul id="nol_menuGlobal" class="nol_menuBtn_common">
				<li class="nol_item1 nol_item_first nol_menuBtn"><span class="nol_item_wrap"><span class="nol_item_inner">番組?????</span></span>
					<div id="nol_Window01" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/hensei/program/?area=001&amp;f=top" onclick="nol_com.noltc('NOL_Header_Bangumihyo');" data-areacode="http://www2.nhk.or.jp/hensei/program/?area={{areacode}}&amp;f=top"><span class="nol_navList_hd">番組表</span><span class="nol_navList_sub">８日先???過去30日???情報</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/toppage/program_list/" onclick="nol_com.noltc('NOL_Header_ProgramList');"><span class="nol_navList_hd">番組名一?</span><span class="nol_navList_sub">五十音順?一???</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www6.nhk.or.jp/nhkpr/" onclick="nol_com.noltc('NOL_Header_NHKPR');"><span class="nol_navList_hd">ＮＨＫ＿ＰＲ</span><span class="nol_navList_sub">?報局???????</span></a></div></li>
							</ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_item2 nol_menuBtn" style="display: none;"><span class="nol_item_wrap"><span class="nol_item_inner">????視?</span></span>
					<div id="nol_Window02" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="https://www.nhk-ondemand.jp/" onclick="nol_com.noltc('NOL_Header_NOD');"><span class="nol_navList_hd">ＮＨＫ??????</span><span class="nol_navList_sub">番組?動?配信</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/d-garage/" onclick="nol_com.noltc('NOL_Header_Dgarage');"><span class="nol_navList_hd">??????</span><span class="nol_navList_sub">???動??????????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/ten5/" onclick="nol_com.noltc('NOL_Header_ten5');"><span class="nol_navList_hd">ＮＨＫ１.５ｃｈ</span><span class="nol_navList_sub">????????濃縮</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/radio/" onclick="nol_com.noltc('NOL_Header_radio');"><span class="nol_navList_hd">ＮＨＫ???　???★???</span><span class="nol_navList_sub">???????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/archives/" onclick="nol_com.noltc('NOL_Header_Archives');"><span class="nol_navList_hd">ＮＨＫ??????</span><span class="nol_navList_sub">?????映像</span></a></div></li>
							</ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_item3 nol_menuBtn" style="display: none;"><span class="nol_item_wrap"><span class="nol_item_inner">知???</span></span>
					<div id="nol_Window03" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="https://www2.nhk.or.jp/gogaku/" onclick="nol_com.noltc('NOL_Header_Gogaku');"><span class="nol_navList_hd">???</span><span class="nol_navList_sub">語?講座??合案?</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/kokokoza/" onclick="nol_com.noltc('NOL_Header_Kokokoza');"><span class="nol_navList_hd">高校講座</span><span class="nol_navList_sub">自?自習??????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/lifestyle/" onclick="nol_com.noltc('NOL_Footer_lifestyle');"><span class="nol_navList_hd">???</span><span class="nol_navList_sub">????豊????情報</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/kenko/" onclick="nol_com.noltc('NOL_Header_Kenko');"><span class="nol_navList_hd">健康?????</span><span class="nol_navList_sub">確???療?健康情報?</span></a></div></li>
							</ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_item4 nol_menuBtn" style="display: none;"><span class="nol_item_wrap"><span class="nol_item_inner">報道?????</span></span>
					<div id="nol_Window04" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="https://www3.nhk.or.jp/news/" onclick="nol_com.noltc('NOL_Header_News');"><span class="nol_navList_hd">ＮＥＷＳ ＷＥＢ</span><span class="nol_navList_sub">ＮＨＫ?????記事?見????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www3.nhk.or.jp/lnews/" onclick="nol_com.noltc('NOL_Header_Lnews');"><span class="nol_navList_hd">各地?????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="https://www1.nhk.or.jp/sports/" onclick="nol_com.noltc('NOL_Header_Sports');"><span class="nol_navList_hd">?????????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/shuwa/" onclick="nol_com.noltc('NOL_Header_Shuwa');"><span class="nol_navList_hd">手話????</span><span class="nol_navList_sub">動??見????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/kaisetsu/" onclick="nol_com.noltc('NOL_Header_Kaisetsu');"><span class="nol_navList_hd">解?委員室</span><span class="nol_navList_sub">時代?見??、社?????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/senkyo/" onclick="nol_com.noltc('NOL_Header_Senkyo');"><span class="nol_navList_hd">選?ＷＥＢ</span><span class="nol_navList_sub">選??????</span></a></div></li>
							</ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_item5 nol_menuBtn" style="display: none;"><span class="nol_item_wrap"><span class="nol_item_inner">?加??募??</span></span>
					<div id="nol_Window05" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="https://hh.pid.nhk.or.jp/pidh10/eventList.do" onclick="nol_com.noltc('NOL_Header_Eventinfo');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">番組????????申???</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www2.nhk.or.jp/toppage/bosyu/" onclick="nol_com.noltc('NOL_Header_Bosyu');"><span class="nol_navList_hd">投稿募集一?</span><span class="nol_navList_sub">????????????募集</span></a></div></li><li><div class="nol_navList_inner"><a href="https://pid.nhk.or.jp/pid03/loginform.do?href=https%3A%2F%2Fwww3.nhk.or.jp%2Fnews%2Feasy%2F" onclick="nol_com.noltc('NOL_Header_Netclub');"><span class="nol_navList_hd">ＮＨＫ??????：????</span><span class="nol_navList_sub">便利??員????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/css/" onclick="nol_com.noltc('NOL_Header_CSS');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">?意見??問?合??????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://pid.nhk.or.jp/pid05/enqueteList.do" onclick="nol_com.noltc('NOL_Header_Enquete');"><span class="nol_navList_hd">?????一?</span><span class="nol_navList_sub">?加?希望?方??????</span></a></div></li>
							</ul></div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_item6 nol_menuBtn" style="display: none;"><span class="nol_item_wrap"><span class="nol_item_inner">????問?合??</span></span>
					<div id="nol_Window06" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul class="nol_navList">
								<li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/css/" onclick="nol_com.noltc('NOL_Header_CSS');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">?意見??問?合??????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://pid.nhk.or.jp/cas/" onclick="nol_com.noltc('NOL_Header_Bcas');"><span class="nol_navList_hd">ＢＳ?????消去</span><span class="nol_navList_sub">?????消去?申??口</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/goods/pc/cgi/" onclick="nol_com.noltc('NOL_Header_Goods');"><span class="nol_navList_hd">番組?連???</span><span class="nol_navList_sub">?????DVD???一?</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/info/" onclick="nol_com.noltc('NOL_Header_AboutNHK');"><span class="nol_navList_hd">ＮＨＫ????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/faq-corner/" onclick="nol_com.noltc('NOL_Header_Faq');"><span class="nol_navList_hd">????質問集</span><span class="nol_navList_sub"></span></a></div></li>
							</ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
				<li class="nol_itemMore nol_menuBtn" style="display: list-item;"><span class="nol_item_wrap"><span class="nol_item_inner">…???</span></span>
					<div id="nol_WindowMore" class="nol_modalWindow">
						<div class="nol_navList_wrap">
							<ul id="nol_subGlobal">
								<li id="nol_subitem01" class="nol_menuBtn_sub nol_active"><span class="nol_subGlobal_inner">番組?????</span></li><li id="nol_subitem02" class="nol_menuBtn_sub"><span class="nol_subGlobal_inner">????視?</span></li><li id="nol_subitem03" class="nol_menuBtn_sub"><span class="nol_subGlobal_inner">知???</span></li><li id="nol_subitem04" class="nol_menuBtn_sub"><span class="nol_subGlobal_inner">報道?????</span></li><li id="nol_subitem05" class="nol_menuBtn_sub"><span class="nol_subGlobal_inner">?加??募??</span></li><li id="nol_subitem06" class="nol_menuBtn_sub"><span class="nol_subGlobal_inner">????問?合??</span></li>
							</ul>
							<div id="nol_subWindow01" class="nol_modalWindow_more nol_show">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/hensei/program/?area=001&amp;f=top" onclick="nol_com.noltc('NOL_Header_Bangumihyo');" data-areacode="http://www2.nhk.or.jp/hensei/program/?area={{areacode}}&amp;f=top"><span class="nol_navList_hd">番組表</span><span class="nol_navList_sub">８日先???過去30日???情報</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/toppage/program_list/" onclick="nol_com.noltc('NOL_Header_ProgramList');"><span class="nol_navList_hd">番組名一?</span><span class="nol_navList_sub">五十音順?一???</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www6.nhk.or.jp/nhkpr/" onclick="nol_com.noltc('NOL_Header_NHKPR');"><span class="nol_navList_hd">ＮＨＫ＿ＰＲ</span><span class="nol_navList_sub">?報局???????</span></a></div></li>
									</ul>
								</div>
								<p class="nol_close">閉??</p>
							</div>
							<div id="nol_subWindow02" class="nol_modalWindow_more">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="https://www.nhk-ondemand.jp/" onclick="nol_com.noltc('NOL_Header_NOD');"><span class="nol_navList_hd">ＮＨＫ??????</span><span class="nol_navList_sub">番組?動?配信</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/d-garage/" onclick="nol_com.noltc('NOL_Header_Dgarage');"><span class="nol_navList_hd">??????</span><span class="nol_navList_sub">???動??????????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/ten5/" onclick="nol_com.noltc('NOL_Header_ten5');"><span class="nol_navList_hd">ＮＨＫ１.５ｃｈ</span><span class="nol_navList_sub">????????濃縮</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/radio/" onclick="nol_com.noltc('NOL_Header_radio');"><span class="nol_navList_hd">ＮＨＫ???　???★???</span><span class="nol_navList_sub">???????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/archives/" onclick="nol_com.noltc('NOL_Header_Archives');"><span class="nol_navList_hd">ＮＨＫ??????</span><span class="nol_navList_sub">?????映像</span></a></div></li>
									</ul>
								</div>
								<p class="nol_close">閉??</p>
							</div>
							<div id="nol_subWindow03" class="nol_modalWindow_more">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="https://www2.nhk.or.jp/gogaku/" onclick="nol_com.noltc('NOL_Header_Gogaku');"><span class="nol_navList_hd">???</span><span class="nol_navList_sub">語?講座??合案?</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/kokokoza/" onclick="nol_com.noltc('NOL_Header_Kokokoza');"><span class="nol_navList_hd">高校講座</span><span class="nol_navList_sub">自?自習??????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/lifestyle/" onclick="nol_com.noltc('NOL_Footer_lifestyle');"><span class="nol_navList_hd">???</span><span class="nol_navList_sub">????豊????情報</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/kenko/" onclick="nol_com.noltc('NOL_Header_Kenko');"><span class="nol_navList_hd">健康?????</span><span class="nol_navList_sub">確???療?健康情報?</span></a></div></li>
									</ul>
								</div>
								<p class="nol_close">閉??</p>
							</div>
							<div id="nol_subWindow04" class="nol_modalWindow_more">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="https://www3.nhk.or.jp/news/" onclick="nol_com.noltc('NOL_Header_News');"><span class="nol_navList_hd">ＮＥＷＳ ＷＥＢ</span><span class="nol_navList_sub">ＮＨＫ?????記事?見????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www3.nhk.or.jp/lnews/" onclick="nol_com.noltc('NOL_Header_Lnews');"><span class="nol_navList_hd">各地?????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="https://www1.nhk.or.jp/sports/" onclick="nol_com.noltc('NOL_Header_Sports');"><span class="nol_navList_hd">?????????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/shuwa/" onclick="nol_com.noltc('NOL_Header_Shuwa');"><span class="nol_navList_hd">手話????</span><span class="nol_navList_sub">動??見????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/kaisetsu/" onclick="nol_com.noltc('NOL_Header_Kaisetsu');"><span class="nol_navList_hd">解?委員室</span><span class="nol_navList_sub">時代?見??、社?????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www.nhk.or.jp/senkyo/" onclick="nol_com.noltc('NOL_Header_Senkyo');"><span class="nol_navList_hd">選?ＷＥＢ</span><span class="nol_navList_sub">選??????</span></a></div></li>
									</ul>
								</div>
								<p class="nol_close">閉??</p>
							</div>
							<div id="nol_subWindow05" class="nol_modalWindow_more">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="https://hh.pid.nhk.or.jp/pidh10/eventList.do" onclick="nol_com.noltc('NOL_Header_Eventinfo');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">番組????????申???</span></a></div></li><li><div class="nol_navList_inner"><a href="https://www2.nhk.or.jp/toppage/bosyu/" onclick="nol_com.noltc('NOL_Header_Bosyu');"><span class="nol_navList_hd">投稿募集一?</span><span class="nol_navList_sub">????????????募集</span></a></div></li><li><div class="nol_navList_inner"><a href="https://pid.nhk.or.jp/pid03/loginform.do?href=https%3A%2F%2Fwww3.nhk.or.jp%2Fnews%2Feasy%2F" onclick="nol_com.noltc('NOL_Header_Netclub');"><span class="nol_navList_hd">ＮＨＫ??????：????</span><span class="nol_navList_sub">便利??員????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/css/" onclick="nol_com.noltc('NOL_Header_CSS');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">?意見??問?合??????</span></a></div></li><li><div class="nol_navList_inner"><a href="https://pid.nhk.or.jp/pid05/enqueteList.do" onclick="nol_com.noltc('NOL_Header_Enquete');"><span class="nol_navList_hd">?????一?</span><span class="nol_navList_sub">?加?希望?方??????</span></a></div></li>
									</ul></div>
								<p class="nol_close">閉??</p>
							</div>
							<div id="nol_subWindow06" class="nol_modalWindow_more">
								<div class="nol_navList_wrap">
									<ul class="nol_navList">
										<li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/css/" onclick="nol_com.noltc('NOL_Header_CSS');"><span class="nol_navList_hd">?????????????</span><span class="nol_navList_sub">?意見??問?合??????</span></a></div></li><li><div class="nol_navList_inner"><a href="http://pid.nhk.or.jp/cas/" onclick="nol_com.noltc('NOL_Header_Bcas');"><span class="nol_navList_hd">ＢＳ?????消去</span><span class="nol_navList_sub">?????消去?申??口</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www2.nhk.or.jp/goods/pc/cgi/" onclick="nol_com.noltc('NOL_Header_Goods');"><span class="nol_navList_hd">番組?連???</span><span class="nol_navList_sub">?????DVD???一?</span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/info/" onclick="nol_com.noltc('NOL_Header_AboutNHK');"><span class="nol_navList_hd">ＮＨＫ????</span><span class="nol_navList_sub"></span></a></div></li><li><div class="nol_navList_inner"><a href="http://www.nhk.or.jp/faq-corner/" onclick="nol_com.noltc('NOL_Header_Faq');"><span class="nol_navList_hd">????質問集</span><span class="nol_navList_sub"></span></a></div></li>
									</ul>
								</div>
								<p class="nol_close">閉??</p>
							</div>
							<ul class="nol_navList"> </ul>
						</div>
						<p class="nol_close">閉??</p>
					</div>
				</li>
			</ul>
		</div>
		<ul id="nol_searchArea" class="">
			<li id="nol_menuSearch_select" class="nol_item8">
				<div class="nol_item_wrap">
					<p id="nol_pref_hd">地域：</p>
					<p id="nol_pref">東京</p>
					<p id="nol_pref_config"><img src="//www.nhk.or.jp/common/res/img2/icon_select.png" alt="" /> </p>
				</div>
				<div id="nol_prefSetting" class="nol_modalWindow">
					<div id="nol_prefSettingInner" class="nol_modalWindowInner" style="cursor: auto;">
						<div id="nol_prefSetting_select01">
							<p class="nol_text">???????地域?選???????。
								<br />選???地域?「番組表」?自動的?表示????。</p>
							<p id="nol_nowSetting"><strong>現在設定中?地域 ：</strong><span id="nol_prefCall">東京<span>（首都?放送????）</span></span>
							</p>
							<div class="nol_prefSettingArea">
								<p id="nol_prefList1_tag">
									<select id="nol_prefList1">
										<option value="700">北海道：札幌</option><option value="701">北海道：函館</option><option value="702">北海道：旭川</option><option value="703">北海道：??</option><option value="704">北海道：釧路</option><option value="705">北海道：北見</option><option value="706">北海道：室蘭</option><option value="608">青森</option><option value="604">岩手</option><option value="600">宮城</option><option value="601">秋田</option><option value="602">山形</option><option value="605">福島</option><option value="107">茨城</option><option value="109">?木</option><option value="106">群馬</option><option value="110">埼玉</option><option value="108">千葉</option><option value="001">東京</option><option value="105">神奈川</option><option value="103">新潟</option><option value="306">富山</option><option value="302">石川</option><option value="305">福井</option><option value="104">山梨</option><option value="101">長野</option><option value="308">岐阜</option><option value="303">?岡</option><option value="300">愛知</option><option value="307">三重</option><option value="206">滋賀</option><option value="201">京都</option><option value="200">大阪</option><option value="202">兵庫</option><option value="205">奈良</option><option value="204">和歌山</option><option value="404">鳥取</option><option value="403">島根</option><option value="402">岡山</option><option value="400">?島</option><option value="406">山口</option><option value="802">?島</option><option value="803">香川</option><option value="800">愛媛</option><option value="801">高知</option><option value="501">福岡</option><option value="502">福岡：北九州</option><option value="508">佐賀</option><option value="503">長崎</option><option value="500">熊本</option><option value="507">大分</option><option value="506">宮崎</option><option value="505">鹿?島</option><option value="509">沖?</option>
									</select>
								</p><p id="nol_prefSetting_all"><img src="//www.nhk.or.jp/common/res/img2/bt_select_all.png" alt="一括設定" /> </p>
							</div>
						</div>
					</div>
					<p class="nol_close">閉??</p>
				</div>
			</li>
			<li id="nol_menuSearch_input" class="nol_item9">
				<form action="https://www2.nhk.or.jp/cgisearch/wbs/query.cgi" method="get" name="seek" id="nol_seek" onsubmit="nol_com.noltc('NOL_Header_Search');">
					<input type="hidden" name="col" value="top" />
					<input type="hidden" name="ct" value="" />
					<input type="hidden" name="st" value="" />
					<input type="hidden" name="ql" value="" />
					<input type="hidden" name="charset" value="utf-8" />
					<input type="text" class="nol_wordInputArea" maxlength="2047" size="20" name="qt" placeholder="NHK 全体???索" />
					<input width="33" type="button" id="nol_search" class="nol_btSearch" name="search" alt="?索" />
				</form>
			</li>
		</ul>
		<div id="nol_headerGroup02">
			<ul id="nol_menuNav" class="nol_menuBtn_common">
				<li class="nol_item6 nol_item_first"><span class="nol_item_inner"><a href="http://pid.nhk.or.jp/jushinryo/" onclick="nol_com.noltc('NOL_Header_Jushinryo');">受信料??口</a></span> </li>
				<li class="nol_item7"><span class="nol_item_inner"><a href="http://www.nhk.or.jp/toppage/sitemap/" onclick="nol_com.noltc('NOL_Header_Sitemap');">??????</a></span> </li>
			</ul>
		</div>
	</div>
	<div id="nol_emergencyNews" style="display:none;"></div>
	<div id="nol_deviceLabel" style="display:none;min-width: 980px; box-sizing: border-box; padding: 12px 10px; margin: 0; background-color:#fff;"></div>
</div></div>
</aside>
<div id="wrapper" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;">
  <div id="content" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;">
    <div class="easy-wrapper" id="easy-wrapper">
      <div id="mediaFlg"></div>
      <header class="easy-header">
        <div class="easy-header-title">
          <div class="easy-header-title__inner">
            <h1 class="easy-header-title__title">
              <a href="./">
                <img src="./images/logo_pc.png" alt="NEWS WEB EASY" class="easy-logo" />
              </a>
              <img src="./images/subtitle_pc.png" alt="????日本語?書??????" class="easy-subtitle" />
            </h1>
          </div>
        </div>
        <a href="#disaster-list" class="link-to-disaster js-smooth-scroll show-sp"><ruby>災害<rt>????</rt></ruby>?<ruby>?<rt>?</rt></ruby>????</a>
        <div class="header-about-easy js-accordion-wrapper">
          <div class="header-about-easy__inner">
            <a href="#" class="header-about-easy__toggle js-toggle-accordion">
              <!-- <i><img src="./images/icon_about_pc.png" alt="?"></i> -->
              NEWS WEB EASY????
            </a>
          </div>
          <div class="header-about-easy__body about-easy-body js-accordion-body">
            <div class="about-easy-body__inner">
              <p>
                「ＮＥＷＳ ＷＥＢ ＥＡＳＹ」?<ruby>外?人<rt>??????</rt></ruby>?<ruby>皆<rt>??</rt></ruby>???、<ruby>小?生<rt>???????</rt></ruby>?<ruby>中?生<rt>???????</rt></ruby>?<ruby>皆<rt>??</rt></ruby>??????、???????????????<ruby>伝<rt>??</rt></ruby>???。
              </p>
            </div>
          </div>
        </div>
      </header>
      <div class="l-container">

        <main class="l-main">
          <section class="top-news-list">
            <div class="top-news-list__pickup news-list-item" id="js-news-pickup"><figure class="news-list-item__image"><a href="./k10011771341000/k10011771341000.html"><img src="https://www3.nhk.or.jp/news/html/20190108/../20190108/K10011771341_1901082103_1901082113_01_03.jpg" alt="" onerror="this.src='./images/noimg_default_easy.png';" /></a></figure><h1 class="news-list-item__title is-pickup"><a href="./k10011771341000/k10011771341000.html"><em class="title"><ruby>西野<rt>???</rt></ruby>?????<ruby>歌手<rt>???</rt></ruby>?????<ruby>休<rt>??</rt></ruby>?</em><time class="time">1月9日 16時30分</time></a></h1></div>
            <ul class="top-news-list__items news-list-grid" id="js-news-summary"><li class="news-list-grid__item news-list-item"><figure class="news-list-item__image"><a href="./k10011771121000/k10011771121000.html"><img src="./k10011771121000/k10011771121000.jpg" alt="" onerror="this.src='./images/noimg_default_easy.png';" /></a></figure><h1 class="news-list-item__title"><a href="./k10011771121000/k10011771121000.html"><em class="title">??????<ruby>金<rt>??</rt></ruby>????<ruby>取<rt>?</rt></ruby>??<ruby>吉田<rt>???</rt></ruby><ruby>沙保里<rt>???</rt></ruby>???<ruby>選手<rt>????</rt></ruby>????</em><time class="time">1月9日 16時30分</time></a></h1></li><li class="news-list-grid__item news-list-item"><figure class="news-list-item__image"><a href="./k10011771681000/k10011771681000.html"><img src="https://www3.nhk.or.jp/news/html/20190109/../20190109/K10011771681_1901090541_1901090541_01_03.jpg" alt="" onerror="this.src='./images/noimg_default_easy.png';" /></a></figure><h1 class="news-list-item__title"><a href="./k10011771681000/k10011771681000.html"><em class="title">「???」?<ruby>台?<rt>????</rt></ruby>????????????????</em><time class="time">1月9日 16時30分</time></a></h1></li><li class="news-list-grid__item news-list-item"><figure class="news-list-item__image"><a href="./k10011770391000/k10011770391000.html"><img src="https://www3.nhk.or.jp/news/html/20190108/../20190108/K10011770391_1901080032_1901080458_01_02.jpg" alt="" onerror="this.src='./images/noimg_default_easy.png';" /></a></figure><h1 class="news-list-item__title"><a href="./k10011770391000/k10011770391000.html"><em class="title">「<ruby>結婚<rt>????</rt></ruby>???????」?６８％　ＮＨＫ?<ruby>調<rt>??</rt></ruby>??</em><time class="time">1月9日 11時30分</time></a></h1></li><li class="news-list-grid__item news-list-item"><figure class="news-list-item__image"><a href="./k10011770241000/k10011770241000.html"><img src="https://www3.nhk.or.jp/news/html/20190107/../20190107/K10011770241_1901071940_1901071948_01_03.jpg" alt="" onerror="this.src='./images/noimg_default_easy.png';" /></a></figure><h1 class="news-list-item__title"><a href="./k10011770241000/k10011770241000.html"><em class="title">?????????<ruby>?<rt>?</rt></ruby>????　<ruby>別府市<rt>????</rt></ruby>?????<ruby>作<rt>??</rt></ruby>?</em><time class="time">1月9日 11時30分</time></a></h1></li></ul>
          </section>
        </main>
        <aside class="l-sidebar sidebar">
          
            <section class="sidebar-section side-disaster hide-sp">
              <h1 class="sidebar-section__title"><ruby>災害<rt>????</rt></ruby>?<ruby>?<rt>?</rt></ruby>????</h1>
              <ul class="disaster-list js-disaster-list">
              <li class="side-disaster-item side-disaster-earthquake"><a href="#" class="disaster-link has-child"><span class="side-disaster-icon"><img src="./images/icon_disaster_earthquake_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby></em></a><a href="./article/disaster_earthquake_01.html" class="disaster-link-child"><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby>?<ruby>起<rt>?</rt></ruby>????</em></a><a href="./article/disaster_earthquake_02.html" class="disaster-link-child"><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby>?<ruby>?<rt>?</rt></ruby>?<ruby>前<rt>??</rt></ruby>???????</em></a></li><li class="side-disaster-item side-disaster-tsunami"><a href="./article/disaster_tsunami.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_tsunami_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>津波<rt>???</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-tornado"><a href="./article/disaster_tornado.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_tornado_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>??<rt>????</rt></ruby>?<ruby>雷<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-typhoon"><a href="./article/disaster_typhoon.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_typhoon_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>台風<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-rain"><a href="./article/disaster_rain.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_rain_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>大雨<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-snow"><a href="./article/disaster_snow.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_snow_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>大雪<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-heat"><a href="./article/disaster_heat.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_heat_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>熱中症<rt>????????</rt></ruby></em></a></li></ul>
            </section>

                      <section class="sidebar-section archives">
              <h1 class="sidebar-section__title">１?<ruby>月<rt>??</rt></ruby>?????</h1>
              <div class="archives-pager">
                <a href="#" class="archives-pager__arrow is-prev js-pager-nav"><ruby>次<rt>??</rt></ruby>?<ruby>日<rt>?</rt></ruby></a>
                <p class="archives-pager__date" id="js-pager-date">1月8日</p>
                <a href="#" class="archives-pager__arrow is-next js-pager-nav"><ruby>前<rt>??</rt></ruby>?<ruby>日<rt>?</rt></ruby></a>
              </div>
              <div class="archives-list" id="js-archives-list"><a href="./k10011770571000/k10011770571000.html" class="side-news-list__item side-news-item"><img src="https://www3.nhk.or.jp/news/html/20190108/../20190108/K10011770571_1901080850_1901080856_01_02.jpg" alt="" class="side-news-item__image" onerror="this.src='./images/noimg_default_easy_s.png';" /><em class="side-news-item__title">「<ruby>?野古<rt>???</rt></ruby>?<ruby>工事<rt>???</rt></ruby>?<ruby>中止<rt>????</rt></ruby>??」　????????<ruby>前<rt>??</rt></ruby>?<ruby>集<rt>??</rt></ruby>??</em></a><a href="./k10011769971000/k10011769971000.html" class="side-news-list__item side-news-item"><img src="https://www3.nhk.or.jp/news/html/20190107/../20190107/K10011769971_1901071613_1901071618_01_02.jpg" alt="" class="side-news-item__image" onerror="this.src='./images/noimg_default_easy_s.png';" /><em class="side-news-item__title"><ruby>今年<rt>???</rt></ruby>?<ruby>健康<rt>????</rt></ruby>?<ruby>祈<rt>??</rt></ruby>??「<ruby>七草<rt>????</rt></ruby>??」?<ruby>食<rt>?</rt></ruby>??</em></a><a href="./k10011770331000/k10011770331000.html" class="side-news-list__item side-news-item"><img src="https://www3.nhk.or.jp/news/html/20190107/../20190107/K10011770331_1901080035_1901080037_01_02.jpg" alt="" class="side-news-item__image" onerror="this.src='./images/noimg_default_easy_s.png';" /><em class="side-news-item__title"><ruby>???<rt>????</rt></ruby><ruby>寂?<rt>??????</rt></ruby>??「<ruby>我慢<rt>???</rt></ruby>??????????????」</em></a><a href="./k10011768591000/k10011768591000.html" class="side-news-list__item side-news-item"><img src="./k10011768591000/k10011768591000.jpg" alt="" class="side-news-item__image is-easy" onerror="this.src='./images/noimg_default_easy_s.png';" /><em class="side-news-item__title"><ruby>仲邑<rt>????</rt></ruby><ruby>菫<rt>???</rt></ruby>??　????<ruby>若<rt>??</rt></ruby>?１０<ruby>?<rt>??</rt></ruby>?<ruby>?碁<rt>??</rt></ruby>??????</em></a><a href="./k10011769401000/k10011769401000.html" class="side-news-list__item side-news-item"><img src="./k10011769401000/k10011769401000.jpg" alt="" class="side-news-item__image is-easy" onerror="this.src='./images/noimg_default_easy_s.png';" /><em class="side-news-item__title"><ruby>東京<rt>?????</rt></ruby>?<ruby>山手線<rt>??????</rt></ruby>?<ruby>自動<rt>???</rt></ruby>?<ruby>走<rt>??</rt></ruby>?<ruby>電車<rt>????</rt></ruby>?????<ruby>行<rt>???</rt></ruby>?</em></a></div>
            </section>

          
            <section class="sidebar-section side-disaster show-sp" id="disaster-list">
              <h1 class="sidebar-section__title"><ruby>災害<rt>????</rt></ruby>?<ruby>?<rt>?</rt></ruby>????</h1>
              <ul class="disaster-list js-disaster-list">
              <li class="side-disaster-item side-disaster-earthquake"><a href="#" class="disaster-link has-child"><span class="side-disaster-icon"><img src="./images/icon_disaster_earthquake_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby></em></a><a href="./article/disaster_earthquake_01.html" class="disaster-link-child"><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby>?<ruby>起<rt>?</rt></ruby>????</em></a><a href="./article/disaster_earthquake_02.html" class="disaster-link-child"><em class="side-disaster-title"><ruby>地震<rt>???</rt></ruby>?<ruby>?<rt>?</rt></ruby>?<ruby>前<rt>??</rt></ruby>???????</em></a></li><li class="side-disaster-item side-disaster-tsunami"><a href="./article/disaster_tsunami.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_tsunami_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>津波<rt>???</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-tornado"><a href="./article/disaster_tornado.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_tornado_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>??<rt>????</rt></ruby>?<ruby>雷<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-typhoon"><a href="./article/disaster_typhoon.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_typhoon_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>台風<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-rain"><a href="./article/disaster_rain.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_rain_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>大雨<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-snow"><a href="./article/disaster_snow.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_snow_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>大雪<rt>????</rt></ruby></em></a></li><li class="side-disaster-item side-disaster-heat"><a href="./article/disaster_heat.html" class="disaster-link"><span class="side-disaster-icon"><img src="./images/icon_disaster_heat_pc.png" alt="" class="js-responsive-image" /></span><em class="side-disaster-title"><ruby>熱中症<rt>????????</rt></ruby></em></a></li></ul>
            </section>

                      <section class="sidebar-section side-about-easy show-sp js-accordion-wrapper">
              <a href="#" class="side-about-easy__toggle js-toggle-accordion">NEWS WEB EASY????</a>
              <div class="side-about-easy__body js-accordion-body">
                <p>
                  「ＮＥＷＳ ＷＥＢ ＥＡＳＹ」?<ruby>外?人<rt>??????</rt></ruby>?<ruby>皆<rt>??</rt></ruby>???、<ruby>小?生<rt>???????</rt></ruby>?<ruby>中?生<rt>???????</rt></ruby>?<ruby>皆<rt>??</rt></ruby>??????、???????????????<ruby>伝<rt>??</rt></ruby>??????????。
                </p>
              </div>
            </section>
            <section class="sidebar-section about-dictionary js-accordion-wrapper">
              <a href="#" class="about-dictionary__toggle js-toggle-accordion"><ruby>?書<rt>???</rt></ruby>????</a>
              <div class="about-dictionary__body js-accordion-body">
                <p>
                  「NEWS WEB EASY」??、<ruby>三省堂<rt>??????</rt></ruby>?『<ruby>例解小??語?典第<rt>?????????????????</rt></ruby>5<ruby>版<rt>??</rt></ruby>』?<ruby>使<rt>??</rt></ruby>?????。<br />
                  <ruby>?書<rt>???</rt></ruby>?<ruby>著作?<rt>??????</rt></ruby>?、<ruby>?書<rt>???</rt></ruby>?<ruby>作<rt>??</rt></ruby>??<ruby>株式?社<rt>????????</rt></ruby>　<ruby>三省堂<rt>??????</rt></ruby>?????。
                </p>
              </div>
            </section>

                      <nav class="sidebar-section link-banners">
              <a href="https://www3.nhk.or.jp/news/" class="link-banners__item is-newsweb">
                <img src="./images/banner_newsweb_pc.png" alt="NHK NEWS WEB" class="js-responsive-image" />
              </a>
            </nav>

        </aside>

        
      </div>
    </div>
    <aside id="nhkfooter" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;">
      <script>
          nol_showCmnFooter({
              mode: 'simple'
          });
      </script><div id="nolCmnFooterSection" style="max-width: 100%; width: 100%; padding: 0px; margin: 0px;"><div id="nol_contentsFooter" class="pattern2">
	
	
	<div id="nol_footer" class="w1200">
		<div id="nol_footerInner" style="max-width: 100%; width: 100%;">
			<div class="nol_table">
					<div class="nol_copy_wrap">
						<p class="nol_footerLogo"><a href="https://www.nhk.or.jp/" onclick="nol_com.noltc('NOL_Footer_NhkLogo');"><img width="68" alt="日本放送協?" src="//www.nhk.or.jp/common/res/img2/logo_footer.png" /></a></p>
						<p class="nol_copyright"><span class="nol_copy"><img width="68" alt="Copyright NHK?(Japan Broadcasting Corporation)?All rights reserved.許可???載?????禁???。　??????受信料?制作?????。" src="//www.nhk.or.jp/common/res/img2/logo_footer_copy.png" id="nol_copyA" /><img width="350" alt="Copyright NHK?(Japan Broadcasting Corporation)?All rights reserved.許可???載?????禁???。　??????受信料?制作?????。" src="//www.nhk.or.jp/common/res/img2/logo_footer_copy.png" id="nol_copyB" /></span></p>
					</div>
					<div>
						<ul class="nol_link">
							<li><a class="nol_link" target="_blank" href="http://www.nhk.or.jp/css/" onclick="nol_com.noltc('NOL_Footer_CSS');">?意見??問?合??</a></li><li><a class="nol_link1" target="_blank" href="http://www.nhk.or.jp/privacy/" onclick="nol_com.noltc('NOL_Footer_Privacy');">ＮＨＫ????個人情報保護????</a></li><li><a class="nol_link2" target="_blank" href="http://www.nhk.or.jp/toppage/nhk_info/copyright.html" onclick="nol_com.noltc('NOL_Footer_Copyright');">放送番組?著作?</a></li><li><a class="nol_link3" target="_blank" href="https://www.nhk.or.jp/toppage/rules/" onclick="nol_com.noltc('NOL_Footer_Rules');">ＮＨＫ???????????利用規約</a></li>
						</ul>
					</div>
			</div>
		</div>
	</div>
</div>
</div>
    </aside>
  </div>
  <!--/ #content -->
</div>

<script src="./js/js.cookie.js"></script>
<script src="./js/common.js"></script>

<script src="./js/top.js"></script>
<script src="/news/parts16/js/chartbeat_config.js" charset="UTF-8"></script>
"""