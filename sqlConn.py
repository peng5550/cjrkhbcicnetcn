import pymysql


class connSql(object):

    def __init__(self, host="127.0.0.1", port=3306, usr="root", passwd="123456", database="projects"):
        self.conn = pymysql.connect(host=host, port=port, user=usr, passwd=passwd, db=database,
                                    charset="utf8")
        self.db = self.conn.cursor()

    def __del__(self):
        self.db.close()
        self.conn.close()

    def insert_data(self, table_name, item_info):
        keys = ', '.join(list(item_info.keys()))
        values = ', '.join(['%s'] * len(item_info))
        insert_sql = "insert into `{}`({})values({});".format(table_name, keys, values)

        try:
            self.conn.ping(reconnect=True)
            self.db.execute(insert_sql, tuple(item_info.values()))
            self.conn.commit()
        except Exception as e:
            print(e.args)
            self.conn.rollback()

    def select_data(self, table_name, item_info):
        string_list = []
        for i in item_info.keys():
            string = '%s="%s"' % (i, str(item_info.get(i)))
            string_list.append(string)
        sql_string = ' and '.join(string_list)

        select_sql = "select * from {} where {};".format(table_name, sql_string)
        self.conn.ping(reconnect=True)
        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return res
        else:
            return False

    def select_link(self, table_name):
        res = [
            ('湖北赛港智湾建设工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=243146&sxmc=8'),
            ('襄阳诚山河建筑工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=238050'),
            ('武汉恒联建机工程机械有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=221970'),
            ('武汉宇翔照明工程有限责任公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=221851&sxmc=8'),
            ('武汉锦瑞昊建筑工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=221581'),
            ('武汉腾江电力工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=221415'),
            ('湖北祥驿盛建设工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=221295&sxmc=8'),
            ('武汉铁龙岩土工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=219984'),
            ('武汉金海电力有限责任公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=218298&sxmc=8'),
            ('湖北广楚建设有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=218108&sxmc=8'),
            ('湖北君和伟建设工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=218100'),
            ('湖北鸿鼎伟业建设工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=217874&sxmc=8'),
            ('湖北麓雅建筑装饰工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=216819'),
            ('湖北赛宇建筑安装工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=216813'),
            ('兴山县自来水有限责任公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=216577&sxmc=8'),
            ('湖北仟发建设工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy.aspx?sxbh=213973'),
            ('湖北泓山建筑工程有限公司', 'http://cjrk.hbcic.net.cn/xxgs/QyManage/QysxViewJzy1.aspx?sxbh=212960&sxmc=8')
        ]
        return res
        # select_sql = "select name, comUrl from {} group by name;".format(table_name)
        # self.conn.ping(reconnect=True)
        # self.db.execute(select_sql)
        # res = self.db.fetchall()
        # if res:
        #     return res

    def select_com(self, table_name, comName):
        select_sql = "select * from {} where name='{}';".format(table_name, comName)
        self.conn.ping(reconnect=True)
        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return res


if __name__ == '__main__':
    sql = connSql()
    sql.select_link(table_name="cjrkcompanyinfo")