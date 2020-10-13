from lxml import etree, html
import re

with open("htmlText.html", "r+", encoding="utf-8")as file:
    htmlText = file.read()


html0 = etree.HTML(htmlText)
companyName = html0.xpath("//*[@id='fs1']/table[@class='table']/tr[2]/td/text()")[0].replace("原企业：", "").strip()
print(companyName)
labTDListA = [labTD.xpath("text()")[0].strip() for labTD in html0.xpath("//*[@id='fs2']/table[@class='table']/tr[1]/td")]
labTDListB = [labTD.xpath("text()")[0].strip() for labTD in html0.xpath("//*[@id='fs3']/table[@class='table']/tr[1]/td")]

nameIndexA = labTDListA.index("姓名")
ageIndexA = labTDListA.index("年龄")
majorIndexA = labTDListA.index("职称专业")
posiTitIndexA = labTDListA.index("职称")
nameIndexB = labTDListB.index("姓名")
ageIndexB = labTDListB.index("年龄")
majorIndexB = labTDListB.index("专业")
posiTitIndexB = labTDListB.index("证书编号")


labTRListA = html0.xpath("//*[@id='fs2']/table[@class='table']/tr")[1:]
labTRListB = html0.xpath("//*[@id='fs3']/table[@class='table']/tr")[1:]
for labTR in labTRListA:
    comItem = {
        "name": labTR.xpath("td")[nameIndexA].xpath("text()")[0].strip(),
        "age": labTR.xpath("td")[ageIndexA].xpath("text()")[0].strip(),
        "major": labTR.xpath("td")[majorIndexA].xpath("text()")[0].strip(),
        "posilTitles": labTR.xpath("td")[posiTitIndexA].xpath("text()")[0].strip(),
        "comIink": ""
    }
    print('AAAAAAAAAAAAAAAAAAAAAAA')
    print(comItem)

for labTR in labTRListB:
    comItem = {
        "name": labTR.xpath("td")[nameIndexB].xpath("text()")[0].strip(),
        "age": labTR.xpath("td")[ageIndexB].xpath("text()")[0].strip(),
        "major": labTR.xpath("td")[majorIndexB].xpath("text()")[0].strip(),
        "posilTitles": labTR.xpath("td")[posiTitIndexB].xpath("text()")[0].strip(),
        "comIink": ""
    }
    print("BBBBBBBBBBBBBBBBBBBBBBBB")
    print(comItem)
    print('-' * 100)

tableHtml = html0.xpath("//*[@id='form1']/table/tr[1]/td[1]/table")[0]
[elem.getparent().remove(elem) for elem in tableHtml.xpath("//div[@class='dibu']")]
tableHtmlText = re.sub(r'(<img.*>?)|(<span id="labNowPlace".*?>)', '', html.tostring(tableHtml, encoding="utf-8").decode("utf-8"))
print(tableHtmlText)

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

with open("ddd.html", "w+", encoding="utf-8")as f:
    f.write(f"{htmlMakeOne}\n{tableHtmlText}\n{htmlMakeTwo}")

# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
#
# # 新老版本google兼容
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
# driver.get('http://www.baidu.com')
