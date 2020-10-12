from lxml import etree

with open("htmlText.html", "r+", encoding="utf-8")as file:
    htmlText = file.read()

html = etree.HTML(htmlText)
companyItemList = []
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
        print(index)
        print(comItem)
        print('-' * 100)