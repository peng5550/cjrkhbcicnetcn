
from downloadCompany import CompanyCrawler
from downloadReport import ReportCrawler


def start_task():
    com = CompanyCrawler()
    com.start()
    report = ReportCrawler()
    report.start()



if __name__ == '__main__':
    start_task()