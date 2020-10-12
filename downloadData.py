# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class Login(object):

    def __init__(self):
        """
        初始化
        """
        self.chrome_driver = f"./"
        chrome_options = webdriver.FirefoxOptions()
        # chrome_options.add_argument('-headless')
        chrome_options.add_argument('-no-sandbox')
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"')
        # chrome_options.add_argument('connection="close"')
        self.browser = webdriver.Firefox(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 15)
        self.url = 'http://cjrk.hbcic.net.cn/xxgs/index.aspx'

    def open(self):
        """
        打开网页，输入账号、密码，点击
        """
        print(11111111)
        print(self.url)
        self.browser.get(self.url)
        time.sleep(10)
        print(self.browser.page_source)


    def start(self):
        """
        开始
        """
        # 打开网页
        self.open()


if __name__ == '__main__':

    login = Login()
    login.start()
