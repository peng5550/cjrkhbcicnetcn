# -*- coding: UTF-8 -*-
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree, html
from sqlConn import connSql
import re
import os

DATAPATH = "./data"
TABLENAME = "cjrkcompanyinfo"
sTABLENAME = "cjrkreport"
if not os.path.exists(DATAPATH):
    os.makedirs(DATAPATH)

class ReportCrawler(object):

    def __init__(self):
        self.sql = connSql()

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
        return driver

    def __quit_driver(self, driver):
        # 推出driver
        if driver:
            driver.quit()

    def getUrlFromSql(self):
        urlList = self.sql.select_link(table_name=TABLENAME)
        return [[i[0],i[1]] for i in urlList if i]


    def getHtml(self, driver, wait, link):
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.ID, "form1")))
        htmlText = driver.page_source
        return htmlText

    def dataProcessing(self, htmlText, companyName, link):
        html0 = etree.HTML(htmlText)
        labTDListA = [labTD.xpath("text()")[0].strip() for labTD in
                      html0.xpath("//*[@id='fs2']/table[@class='table']/tbody/tr[1]/td")]
        labTDListB = [labTD.xpath("text()")[0].strip() for labTD in
                      html0.xpath("//*[@id='fs3']/table[@class='table']/tbody/tr[1]/td")]
        nameIndexA = labTDListA.index("姓名")
        ageIndexA = labTDListA.index("年龄")
        majorIndexA = labTDListA.index("职称专业")
        posiTitIndexA = labTDListA.index("职称")
        nameIndexB = labTDListB.index("姓名")
        ageIndexB = labTDListB.index("年龄")
        majorIndexB = labTDListB.index("专业")
        posiTitIndexB = labTDListB.index("证书编号")

        labTRListA = html0.xpath("//*[@id='fs2']/table[@class='table']/tbody/tr")[1:]
        labTRListB = html0.xpath("//*[@id='fs3']/table[@class='table']/tbody/tr")[1:]
        infoReportList = []
        for labTR in labTRListA:
            comItem = {
                "name": labTR.xpath("td")[nameIndexA].xpath("text()")[0].strip(),
                "age": labTR.xpath("td")[ageIndexA].xpath("text()")[0].strip(),
                "major": labTR.xpath("td")[majorIndexA].xpath("text()")[0].strip(),
                "posilTitles": labTR.xpath("td")[posiTitIndexA].xpath("text()")[0].strip(),
                "comLink": companyName
            }
            infoReportList.append(comItem)

        for labTR in labTRListB:
            comItem = {
                "name": labTR.xpath("td")[nameIndexB].xpath("text()")[0].strip(),
                "age": labTR.xpath("td")[ageIndexB].xpath("text()")[0].strip(),
                "major": labTR.xpath("td")[majorIndexB].xpath("text()")[0].strip(),
                "posilTitles": labTR.xpath("td")[posiTitIndexB].xpath("text()")[0].strip(),
                "comLink": companyName
            }
            infoReportList.append(comItem)

        tableHtml = html0.xpath("//*[@id='form1']/table/tbody/tr[1]/td[1]/table")[0]
        [elem.getparent().remove(elem) for elem in tableHtml.xpath("//div[@class='dibu']")]
        tableHtmlText = re.sub(r'(<img.*>?)|(<span id="labNowPlace".*?>)', '',
                               html.tostring(tableHtml, encoding="utf-8").decode("utf-8"))
        htmlMakeOne = '''
        <html>
        <meta charset="utf-8">
        <head>
            <style type="text/css">
                html, body, form
                {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    font-size: 14px;
                    font-family: arial,tahoma,Hiragino Sans GB,Microsoft YaHei,sans-serif;
                    color: #4C4C4C;
                    background-color: White;
                }
                .table
                {
                    border-top: 1px solid #666666;
                    border-left: 1px solid #666666;
                }
                .table td
                {
                    height: 30px;
                    line-height: 25px;
                    border-right: 1px solid #666666;
                    border-bottom: 1px solid #666666;
                    padding-left: 2px;
                }
                .table td.head
                {
                    font-weight: bold;
                    background-color: #D5F1FF;
                }
                .txt
                {
                    border: 1px solid #666666;
                    height: 20px;
                    line-height: 20px;
                }
                .btnSearch
                {
                    width: 100px;
                    height: 26px;
                    border-style: none;
                    background-image: url(../images/zcry/查询.jpg);
                    background-repeat: no-repeat;
                    cursor: pointer;
                }

                .line
                {
                    height: 10px; /*filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#ff0000'); /* IE6,IE7 /
                    -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#ff0000')"; / IE8 */
                }
                .fieldset
                {
                    border: 1px solid #ccc;
                    margin: 1em 0;
                    padding: 1em;
                    display: block;
                    margin-inline-start: 2px;
                    margin-inline-end: 2px;
                    padding-block-start: 0.35em;
                    padding-inline-start: 0.75em;
                    padding-inline-end: 0.75em;
                    padding-block-end: 0.625em;
                    min-inline-size: min-content;
                }
                ul
                {
                    height: 80px;
                    list-style: none;
                    position: fixed;
                    right: -10px;
                    top: 30%;
                    padding: 0;
                    margin: 0;
                    font-size: 12px;
                    padding-right: 10px;
                    margin-bottom: 5px;
                }
                li
                {
                    display: list-item;
                    text-align: -webkit-match-parent;
                }
                ul li
                {
                    margin: 0;
                    padding: 5px;
                    border: 1px solid #ccc;
                    text-align: center;
                    margin: 10px;
                    background-color: #fff4b9;
                }
                ul #tishi
                {
                    border: 0px solid #ccc;
                    background-color: rgba(0, 0, 0, 0.00);
                    font-family: YouYuan;
                    font-size: 12px;
                    color: #3e3b3b;
                    font-weight: 600;
                }

                ul li a
                {
                    text-decoration: none;
                    color: #4C6C9D;
                }
                ul li a:hover
                {
                    color: red;
                }

                .dibu
                {
                    float: left;
                    width: 1140px;
                    margin-top: 17px;
                    height: auto;
                    line-height: 30px;
                    text-align: center;
                    display: block;
                    background-color: #2A70CF;
                    color: White;
                }
            </style>
        </head>
        '''

        htmlMakeTwo = '''
        </html>

        '''
        for item in infoReportList:
            if not self.sql.select_data(table_name=sTABLENAME, item_info=item):
                print(item)
                self.sql.insert_data(table_name=sTABLENAME, item_info=item)

        with open(f"./data/{companyName}.html", "w+", encoding="utf-8")as f:
            f.write(f"{htmlMakeOne}\n{tableHtmlText}\n{htmlMakeTwo}")


    def __crawler(self, urlList):
        driver = self.__create_driver()
        wait = WebDriverWait(driver, 60)
        for name, link in urlList:
            try:
                _content = self.getHtml(driver, wait, link)
                self.dataProcessing(_content, name, link)
            except Exception as e:
                print(e.args)
                with open("exception.txt", "a+", encoding="utf-8")as file:
                    file.write(link+"\n")

    # def __crawler(self, semaphore, link, companyName):
    #     semaphore.acquire()
    #     try:
    #         driver = self.__create_driver()
    #         wait = WebDriverWait(driver, 60)
    #         _content = self.getHtml(driver, wait, link)
    #         self.dataProcessing(_content, companyName, link)
    #         self.__quit_driver(driver)
    #     except Exception as e:
    #         print(e.args)
    #         with open("exception.txt", "a+", encoding="utf-8")as file:
    #             file.write(link+"\n")
    #     semaphore.release()

    def taskManager(self, linkList, func):
        semaphore = threading.Semaphore(2)
        ts = [threading.Thread(target=func, args=(semaphore, link, name,)) for name, link in linkList]
        [t.start() for t in ts]
        [t.join() for t in ts]

    def start(self):
        urlList = self.getUrlFromSql()
        # self.taskManager(urlList, self.__crawler)
        self.__crawler(urlList)

if __name__ == '__main__':
    login = ReportCrawler()
    login.start()
