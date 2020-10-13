# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
from sqlConn import connSql
import time

TABLENAME = "cjrkcompanyinfo"

class CompanyCrawler(object):

    def __init__(self):
        self.sql = connSql()
        self.mainpage = 'http://cjrk.hbcic.net.cn/xxgs/index.aspx'
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

    def start(self):
        self.driver.get(self.mainpage)
        self.driver.maximize_window()
        self.search_data()
        self.goNextPage()

    def search_data(self):
        self.wait.until(EC.presence_of_element_located((By.ID, 'form1')))
        info_sqlx = self.wait.until(EC.element_to_be_clickable((By.ID, 'ddlSqlx')))
        info_sqlx.click()

        sqlx_select = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlSqlx']/option[@value='107']")))
        sqlx_select.click()

        search_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'btnSearch')))
        search_btn.click()

        time.sleep(10)

        self.wait.until(EC.presence_of_element_located((By.ID, 'form1')))
        self.dataProcessing()

    def goNextPage(self):
        now_page = self.driver.find_element_by_id("labNowPage").text
        total_page = self.driver.find_element_by_id("labPageCount").text

        last_page_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'lbtnLast')))
        last_page_btn.click()

        while int(now_page) <= int(total_page):
            print("-----------------当前页：{}---------------------".format(now_page))
            # next_page_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'lbtnNext')))
            # next_page_btn.click()
            pre_page_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'lbtnPre')))
            pre_page_btn.click()
            self.wait.until(EC.presence_of_element_located((By.ID, 'form1')))
            self.dataProcessing()
            now_page = self.driver.find_element_by_id("labNowPage").text
            total_page = self.driver.find_element_by_id("labPageCount").text


    def dataProcessing(self):
        print('--------------dataProcessing---------------')
        htmlText = self.driver.page_source
        html = etree.HTML(htmlText)
        for index, labTR in enumerate(html.xpath("//table[@class='table']/tbody/tr")):
            if index > 0 and index <= 20:
                try:
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
                except:
                    print("http://cjrk.hbcic.net.cn/xxgs/" + labTR.xpath("td[2]/a/@href")[0].strip())


if __name__ == '__main__':
    report = CompanyCrawler()
    report.start()
