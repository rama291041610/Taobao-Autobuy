#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import datetime
import getpass
import time
import re
import os

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"


class Taobao(object):
    def __init__(self):
        self.url = input("Please input the url of the production:\n")
        self.buy_time = input("Time(Formal:yyyy-mm-dd hh:mm:ss):")
        self.need_autopay = input("Do you need pay automatically?(yes/no)")

        if self.buy_time == '':
            self.buy_time = datetime.datetime.now()
        else:
            self.buy_time = datetime.datetime.strptime(self.buy_time, '%Y-%m-%d %H:%M:%S')

        if self.need_autopay == "yes":
            self.pay_pw = getpass.getpass("Password:")

        if "tmall" in self.url:
            self.mall = "tmall"
        else:
            self.mall = "taobao"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()

        self.is_login = 0

    def __del__(self):
        self.driver.quit()

    def load_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def login(self):
        # Login by Scan code
        login_url = "https://login.taobao.com/member/login.jhtml"
        self.load_page(login_url)

        while "https://www.taobao.com/" not in self.driver.current_url:
            time.sleep(1)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Login Successfully.")
        self.is_login = 1

    def buy(self):
        if self.is_login == 0:
            self.login()
        self.load_page(self.url)

        if self.mall == "taobao":
            #"立即购买"的css_selector
            btn_buy = '#J_juValid > div.tb-btn-buy > a'
            #"提交订单"的css_selector
            btn_order = '#submitOrder_1 > div.wrapper > a'
            juhuasuan = '聚划算活动商品，'
        else:
            btn_buy = '#J_LinkBuy'
            btn_order = '#submitOrder_1 > div > a'
            juhuasuan = '您只有在聚划算页面点击“马上抢”，才可享受此商品的优惠价格'

        while True:
            if datetime.datetime.now() >= self.buy_time:
                if juhuasuan in self.driver.page_source:
                    self.driver.refresh()
                    time.sleep(0.008)
                    continue
                try:
                    if self.driver.find_element_by_css_selector(btn_buy):
                        self.driver.find_element_by_css_selector(btn_buy).click()
                except:
                    pass
                try:
                    if self.driver.find_element_by_css_selector(btn_order):
                        self.driver.find_element_by_css_selector(btn_order).click()
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Order Successfully!")
                        break
                except:
                    pass
            else:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Monitoring!")

        if self.need_autopay == "yes":
            self.pay()
        else:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Successfully! Please pay for it!")
            time.sleep(42)

    def pay(self):
        pay_input = "#payPassword_rsainput"
        pay_btn = "#J_authSubmit"

        while True:
            try:
                if self.driver.find_element_by_css_selector(pay_input):
                    self.driver.find_element_by_css_selector(pay_input).send_keys(self.pay_pw)
                    break
            except:
                time.sleep(0.01)

        while True:
            try:
                if self.driver.find_element_by_css_selector(pay_btn):
                    self.driver.find_element_by_css_selector(pay_btn).click()
                    break
            except:
                time.sleep(0.01)

        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Pay Successfully!")
        time.sleep(42)


if __name__ == "__main__":
    t = Taobao()
    t.buy()
