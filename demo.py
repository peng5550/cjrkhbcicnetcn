import os

from sqlConn import connSql
TABLENAME = "cjrkcompanyinfo"
sql = connSql()

filenameList = [i.strip(".html") for i in os.listdir("./data")]

res = sql.select_link(TABLENAME)

lll = [i for i in res]

for i in lll:
    if i[0] not in filenameList:
        print(f"('{i[0]}', '{i[1]}'),")