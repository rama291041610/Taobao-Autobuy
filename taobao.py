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
        self.need_autopay = input("Do you need pay automatically?yes/no")

        if self.need_autopay == "yes":
            self.pay_pw = getpass.getpass("Password:")

        if "detail.tmall.com" in self.url:
            self.mall = "tmall"
        else:
            self.mall = "taobao"

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.is_login = 0

    def login(self):
        # Login by Scan code
        print("Please login!")

        login_url = "https://login.taobao.com/member/login.jhtml"
        self.driver.get(login_url)
        self.driver.implicitly_wait(10)

        while "https://www.taobao.com/" not in self.driver.current_url:
            time.sleep(1)
        username = re.search("<strong class=\"J_MemberNick member-nick\">(.*?)</strong>", self.driver.page_source)
        if username:
            print("Login account:", username.group(1))
            self.is_login = 1
        else:
            print("Login failed.")
            # self.login()

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
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') >= self.buy_time:
                try:
                    if self.driver.find_element_by_css_selector(btn_buy):
                        self.driver.find_element_by_css_selector(btn_buy).click()
                        break
                    time.sleep(0.03)
                except:
                    # self.driver.refresh()
                    # self.driver.implicitly_wait(0.5)
                    time.sleep(0.1)
            else:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "Monitoring!")

        while True:
            try:
                # Find "立即下单"，Click，
                if self.driver.find_element_by_css_selector(btn_order):
                    self.driver.find_element_by_css_selector(btn_order).click()
                    break
            except:
                time.sleep(0.01)

        if self.need_autopay == "yes":
            self.pay()
        else:
            print("Successfully! Please pay for it!")

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

        print("Pay Successfully!")


if __name__ == "__main__":
    t = Taobao()
    t.buy()
