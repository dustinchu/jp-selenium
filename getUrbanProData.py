#!/usr/bin/env python
# export PATH=$PATH:/home/muru/myFlaskPython
from pyvirtualdisplay import Display
from selenium import webdriver
import time



def get():
    opt=webdriver.ChromeOptions()
    opt.set_headless()
    driver=webdriver.Chrome(options=opt)
    driver.get("https://www3.nhk.or.jp/news/easy/")
    print(driver.page_source)
    time.sleep(5)


    return 'ok'
