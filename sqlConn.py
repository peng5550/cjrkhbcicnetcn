import pymysql


class connSql(object):

    def __init__(self, host="127.0.0.1", port=3306, usr="root", passwd="123456", database="projects"):
        self.conn = pymysql.connect(host=host, port=port, user=usr, passwd=passwd, db=database,
                                    charset="utf8")
        self.db = self.conn.cursor()

    def insert_data(self, table_name, item_info):
        keys = ', '.join(list(item_info.keys()))
        values = ', '.join(['%s'] * len(item_info))
        insert_sql = "insert into `{}`({})values({});".format(table_name, keys, values)

        try:
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

        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return True
        else:
            return False

    def select_link(self, table_name):
        select_sql = "select comUrl from {}".format(table_name)
        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            print(res)
            return res



if __name__ == '__main__':
    sql = connSql()
    sql.select_link(table_name="cjrkcompanyinfo")