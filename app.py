from mttkinter import mtTkinter as mtk
import threading
from tkinter import ttk
from sqlConn import connSql

DATAPATH = "./data"
TABLENAME = "cjrkcompanyinfo"
sTABLENAME = "cjrkreport"


class Application(mtk.Frame):

    def __init__(self, master):
        super(Application, self).__init__()
        self.root = master
        self.root.geometry("500x300")
        self.root.title("查询工具 1.0")
        self.__creatUI()
        self.sql = connSql()

    def __creatUI(self):
        self.searchBox = mtk.LabelFrame(self.root, text="查询", fg="blue")
        self.searchBox.place(x=20, y=15, width=450, height=270)

        self.labName = mtk.Label(self.searchBox, text="姓 名：")
        self.labName.place(x=10, y=10, width=50, height=30)
        self.labNameText = mtk.Entry(self.searchBox)
        self.labNameText.place(x=70, y=10, width=100, height=30)

        self.searchBtn = mtk.Button(self.searchBox, text="查 询")
        self.searchBtn.place(x=250, y=10, width=80, height=30)

        # 数据展示
        title = ['1', '2', '3', '4', '5', '6']
        self.box = ttk.Treeview(self.searchBox, columns=title, show='headings')
        self.box.place(x=10, y=70, width=430, height=170)
        self.box.column('1', width=50, anchor='center')
        self.box.column('2', width=80, anchor='center')
        self.box.column('3', width=50, anchor='center')
        self.box.column('4', width=50, anchor='center')
        self.box.column('5', width=50, anchor='center')
        self.box.column('6', width=100, anchor='center')
        self.box.heading('1', text='序号')
        self.box.heading('2', text='姓名')
        self.box.heading('3', text='年龄')
        self.box.heading('4', text='专业')
        self.box.heading('5', text='职称')
        self.box.heading('6', text='公司名称')
        self.VScroll1 = ttk.Scrollbar(self.box, orient='vertical', command=self.box.yview)
        self.VScroll1.pack(side="right", fill="y")
        self.VScroll2 = ttk.Scrollbar(self.box, orient='horizontal', command=self.box.xview)
        self.VScroll2.pack(side="bottom", fill="x")
        # 给treeview添加配置
        self.box.configure(yscrollcommand=self.VScroll1.set)
        self.box.configure(xscrollcommand=self.VScroll2.set)
        self.box.bind(sequence="<Double-Button-1>", func=lambda x: self.thread_it(self.showCom))

    def __creatUI2(self, comName):
        detailWin = mtk.Toplevel(self.root)
        detailWin.title(comName)
        detailWin.geometry("400x200")
        comInfoBox = mtk.LabelFrame(detailWin, text="任务说明：", fg="blue")
        comInfoBox.place(x=10, y=10, width=380, height=180)
        # 数据展示
        title = ['1', '2', '3', '4']
        self.box2 = ttk.Treeview(detailWin, columns=title, show='headings')
        # style = ttk.Style()
        # style.configure("Treeview.Heading", font=("思源黑体", 11, "bold"))
        self.box2.place(x=10, y=10, width=380, height=150)
        self.box2.column('1', width=50, anchor='center')
        self.box2.column('2', width=50, anchor='center')
        self.box2.column('3', width=100, anchor='center')
        self.box2.column('4', width=100, anchor='center')
        self.box2.heading('1', text='序号')
        self.box2.heading('2', text='类型')
        self.box2.heading('3', text='资质及等级')
        self.box2.heading('4', text='类别')
        self.VScroll1 = ttk.Scrollbar(self.box, orient='vertical', command=self.box.yview)
        self.VScroll1.pack(side="right", fill="y")
        self.box.configure(yscrollcommand=self.VScroll1.set)


    def deleteTree(self):
        x = self.box.get_children()
        for item in x:
            self.box.delete(item)

    def searchData(self, name):
        self.deleteTree()
        search_item = {"name": name}
        res = self.sql.select_data(table_name=sTABLENAME, item_info=search_item)
        if res:
            index = 1
            for item in res:
                item_data = [
                    index,
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5]
                ]
                index += 1
                self.box.insert("", "end", values=item_data)
                self.box.yview_moveto(1.0)

    def showCom(self):
        for item in self.box.selection():
            itemText = self.box.item(item, "values")
            comName = itemText[-1]
            res = self.sql.select_com(table_name=TABLENAME, comName=comName)
            if res:
                index = 1
                for comInfo in res:
                    comItem = [
                        index,
                        comInfo[3],
                        comInfo[4],
                        comInfo[5]
                    ]
                    self.box2.insert("", "end", values=comItem)
                    self.box2.yview_moveto(1.0)

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = mtk.Tk()
    Application(root)
    root.mainloop()