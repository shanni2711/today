import pymysql
import time

class BookManager:
    def __init__(self):
        try:
            self.conn=pymysql.connect(host='localhost',user='root',password='Sry146944$',database='book_db',charset='utf8mb4')
            self.cursor=self.conn.cursor()
            print("数据库连接成功")
        except Exception as e:
            print("数据库连接失败:",e)

    def admin_login(self, admin_name, password):
        sql = "select * from admin where admin_name=%s and password=%s"
        self.cursor.execute(sql, (admin_name, password))
        return self.cursor.fetchone() is not None

    def write_log(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("student_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] {msg}\n")

    def show_all(self):
        sql = "select * from book"
        self.cursor.execute(sql)
        books = self.cursor.fetchall()
        if not books:
            print("暂无图书数据")
            return
        print("\n======= 图书信息列表 =======")
        for s in books:
            print(f"图书编号：{s[0]} | 书名：{s[1]} | 作者：{s[2]} | 分类：{s[3]} | 状态：{s[4]}")

    def add_book(self,book_id,book_name,author,book_sort,book_status):
        try:
            sql="insert into book(book_id,book_name,author,book_sort,book_status) values(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(book_id,book_name,author,book_sort,book_status))
            self.conn.commit()
            print("添加信息成功")
        except Exception as e:
            self.conn.rollback()
            print("请输入正确的信息：",e)

    def select_book(self,book_id):
        sql="select * from book where book_id=%s"
        self.cursor.execute(sql,book_id)
        res=self.cursor.fetchone()
        if res:
            print(f"图书编号：{res[0]},书名：{res[1]},作者：{res[2]},分类:{res[3]},状态：{res[4]}")
        else:
            print("该书不在库内")

    def update_book(self,book_id,book_name,author,book_sort):
        try:
            sql="update book set book_name=%s,author=%s,book_sort=%s where book_id=%s"
            self.cursor.execute(sql,(book_name,author,book_sort,book_id))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("修改成功")
                self.write_log(f"修改图书：{book_id}")
            else:
                print("未找到该图书")
        except Exception as e:
            self.conn.rollback()
            print("请输入正确信息")

    def delete_book(self,book_id):
        try:
            sql="delete from book where book_id=%s"
            self.cursor.execute(sql,book_id)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("删除成功")
                self.write_log(f"删除图书：{book_id}")
            else:
                print("未找到该图书")
        except Exception as e:
            self.conn.rollback()
            print("请输入正确信息：",e)

    def borrow_book(self,book_id):
        sql="select book_status from book where book_id=%s"
        self.cursor.execute(sql,book_id)
        res=self.cursor.fetchone()
        if not res:
            print("图书不存在")
            return
        status=res[0]
        if status == "已借出":
            print("该书已借出，无法借阅")
            return
        sql="update book set book_status='已借出' where book_id=%s"
        self.cursor.execute(sql,book_id)
        self.conn.commit()
        print("借阅成功，状态已更新为：已借出")
        self.write_log(f"借阅图书 ID：{book_id}")

    def return_book(self,book_id):
        sql="select book_status from book where book_id=%s"
        self.cursor.execute(sql, book_id)
        res = self.cursor.fetchone()
        if not res:
            print("图书不存在")
            return
        status=res[0]
        if status=="可借阅":
            print("该书未借出，无需归还")
            return
        sql="update book set book_status='可借阅' where book_id=%s"
        self.cursor.execute(sql,book_id)
        self.conn.commit()
        print("归还成功，状态已更新为：可借阅")
        self.write_log(f"归还图书 ID：{book_id}")


    def close(self):
        self.cursor.close()
        self.conn.close()


def login_system(sm):
    print("======= 管理员登录 =======")
    for i in range(3):
        username = input("请输入账号：")
        password = input("请输入密码：")
        if sm.admin_login(username, password):
            print("登录成功！")
            return True
        else:
            print(f"账号或密码错误，剩余次数：{2-i}")
    print("登录失败，程序退出")
    return False

def main():
    sm = BookManager()
    if not login_system(sm) :
        return

    while True :
        print("\n======= 图书借阅系统 =======")
        print("1. 添加图书")
        print("2. 查询所有图书")
        print("3. 按图书编号查询图书")
        print("4. 修改图书信息")
        print("5. 删除图书")
        print("6. 借阅图书")
        print("7. 归还图书")
        print("0. 退出系统")

        choice = input("请输入功能编号（0-7）：")

        if choice == "1" :
            sid = input("请输入图书编号：")
            name = input("请输入书名：")
            author = input("请输入作者：")
            sort = input("请输入分类：")
            status = input("请输入状态：")
            sm.add_book(sid, name, author, sort, status)

        elif choice == "2" :
            sm.show_all()

        elif choice == "3" :
            sid = input("请输入要查询的图书编号：")
            sm.select_book(sid)

        elif choice == "4" :
            sid = input("请输入要修改的图书编号：")
            name = input("请输入新的书名：")
            author = input("请输入新作者：")
            sort = input("请输入新分类：")
            sm.update_book(sid, name, author, sort)

        elif choice == "5" :
            sid = input("请输入要删除的图书号：")
            sm.delete_book(sid)

        elif choice == "6" :
            sid = input("请输入要借阅的图书号：")
            sm.borrow_book(sid)

        elif choice == "7" :
            sid = input("请输入要归还的图书号：")
            sm.return_book(sid)

        elif choice == "0" :
            sm.close()
            print("系统已退出")
            break
        else :
            print("输入无效，请输入 0-7 之间的数字")

if __name__=="__main__":
    main()
