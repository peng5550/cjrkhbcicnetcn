# -*- coding: UTF-8 -*-
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
import time

from sqlConn import connSql

TABLENAME = "cjrkcompanyinfo"

class ReportCrawler(object):

    def __init__(self):
        self.sql = connSql()
        self.__create_driver()
        self.wait = WebDriverWait(self.driver, 60)

    def __create_driver(self):
        # 创建driver
        options = webdriver.FirefoxOptions()
        options.add_argument(
            'Accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"')
        options.add_argument('Accept-Encoding="gzip, deflate"')
        options.add_argument('Accept-Language="zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"')
        options.add_argument('Connection="keep-alive"')
        # options.add_argument('Content-Type="application/x-www-form-urlencoded"')
        # options.add_argument('Upgrade-Insecure-Requests="1"')
        options.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"')
        # options.add_argument('-headless')
        driver = webdriver.Firefox(firefox_options=options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(10)
        self.driver = driver

    def __quit_driver(self):
        # 推出driver
        if self.driver:
            self.driver.quit()


    # def start(self):
    #     self.driver.get(self.mainpage)
    #     self.driver.maximize_window()
    #     # time.sleep(10)
    #     # print(self.driver.page_source)

    def getUrlFromSql(self):
        urlList = self.sql.select_link(table_name=TABLENAME)
        return [i[0] for i in urlList]


    def getHtml(self, link):
        self.driver.get(link)
        self.wait.until(EC.presence_of_element_located((By.ID, "form1")))
        htmlText = self.driver.page_source
        return htmlText

    def dataProcessing(self, htmlText):
        print('--------------dataProcessing---------------')
        html = etree.HTML(htmlText)
        for index, labTR in enumerate(html.xpath("//table[@class='table']/tbody/tr")):
            if index > 0 and index <= 20:
                comItem = {
                    "name": labTR.xpath("td[2]/a/text()")[0].strip(),
                    "comUrl": "http://cjrk.hbcic.net.cn/xxgs/" + labTR.xpath("td[2]/a/@href")[0].strip(),
                    "cls": "建筑业",
                    "level": ", ".join(labTR.xpath("td[4]/text()")).strip().strip(","),
                    "type": labTR.xpath("td[5]/text()")[0].strip(),
                    "accCom": labTR.xpath("td[6]/text()")[0].strip(),
                    "accDate": labTR.xpath("td[9]/text()")[0].strip(),
                    "accStatus": labTR.xpath("td[10]/text()")[0].strip(),
                }
                item_info = {"comUrl": comItem["comUrl"]}
                if not self.sql.select_data(table_name=TABLENAME, item_info=item_info):
                    self.sql.insert_data(table_name=TABLENAME, item_info=comItem)

    def __crawler(self, semaphore, link):
        semaphore.acquire()
        _content = self.getHtml(link)
        self.dataProcessing(_content)
        semaphore.release()

    def taskManager(self, linkList, func):
        semaphore = threading.Semaphore(2)
        ts = [threading.Thread(target=func, args=(semaphore, link,)) for link in linkList]
        [t.start() for t in ts]
        [t.join() for t in ts]

    def start(self):
        urlList = self.getUrlFromSql()
        self.taskManager(urlList, self.__crawler)

if __name__ == '__main__':
    login = ReportCrawler()
    login.start()
