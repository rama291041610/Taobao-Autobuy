#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import datetime
import time
import re
import os


class Taobao(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.url = input("Please input the url of the production:\n")
        self.buy_time = input("Time(Formal:yyyy-mm-dd hh:mm:ss):")

        if "detail.tmall.com" in self.url:
            self.mall = "tmall"
        else:
            self.mall = "taobao"

        self.is_login = 0

    def login(self):
        # 手动登陆(请使用扫码登陆)
        print("Please login!")

        login_url = "https://login.taobao.com/member/login.jhtml"
        self.driver.get(login_url)
        self.driver.implicitly_wait(10)

        while "https://www.taobao.com/" not in self.driver.current_url:
            time.sleep(5)
        username = re.search("<strong class=\"J_MemberNick member-nick\">(.*?)</strong>", self.driver.page_source)
        if username:
            print("Login account:", username.group(1))
            self.is_login = 1
        else:
            print("Login failed.")
            self.login()

    def buy(self):
        if self.is_login == 0:
            self.login()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        if self.mall == "taobao":
            #"立即购买"的css_selector
            btn_buy = '#J_juValid > div.tb-btn-buy > a'
            #"立即下单"的css_selector
            btn_order = '#submitOrder_1 > div.wrapper > a'
        else:
            btn_buy = '#J_LinkBuy'
            btn_order = '#submitOrder_1 > div > a'

        while True:
            # 现在时间大于预设时间则开售抢购
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') >= self.buy_time:
                try:
                    if self.driver.find_element_by_css_selector(btn_buy):
                        self.driver.find_element_by_css_selector(btn_buy).click()
                        break
                    time.sleep(0.1)
                except:
                    time.sleep(0.3)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Monitoring!")
            self.driver.refresh()
            self.driver.implicitly_wait(0.7)

        while True:
            try:
                # 找到"立即下单"，点击，
                if self.driver.find_element_by_css_selector(btn_order):
                    self.driver.find_element_by_css_selector(btn_order).click()
                if "https://cashiergtj.alipay.com" in self.driver.current_url:
                    self.driver.quit()
                    print("Successfully!Please pay for it!")
                    break
            except:
                time.sleep(0.5)


if __name__ == "__main__":
    t = Taobao()
    t.buy()
