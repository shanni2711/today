
import pymysql
import time

class StudentManager:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sry146944$",
                database="student_db",
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor()
            print("✅ 数据库连接成功")
        except Exception as e:
            print("❌ 数据库连接失败：", e)

    # 管理员登录（从数据库查询验证）
    def admin_login(self, username, password):
        sql = "SELECT * FROM admin_user WHERE username=%s AND password=%s"
        self.cursor.execute(sql, (username, password))
        return self.cursor.fetchone() is not None

    # 日志
    def write_log(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("student_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] {msg}\n")

    # 1. 添加学生
    def add_student(self, stu_id, name, age, major):
        try:
            sql = "INSERT INTO student1(stu_id, name, age, major) VALUES(%s,%s,%s,%s)"
            self.cursor.execute(sql, (stu_id, name, age, major))
            self.conn.commit()
            print("✅ 添加成功")
            self.write_log(f"添加学生：{stu_id} {name}")
        except Exception as e:
            self.conn.rollback()
            print("❌ 添加失败，学号重复或格式错误")

    # 2. 查询所有学生
    def show_all(self):
        sql = "SELECT * FROM student1"
        self.cursor.execute(sql)
        students = self.cursor.fetchall()

        if not students:
            print("暂无学生数据")
            return

        print("\n======= 学生信息列表 =======")
        for s in students:
            print(f"学号：{s[1]} | 姓名：{s[2]} | 年龄：{s[3]} | 专业：{s[4]}")

    # 3. 按学号查询
    def search_by_id(self, stu_id):
        sql = "SELECT * FROM student1 WHERE stu_id=%s"
        self.cursor.execute(sql, stu_id)
        res = self.cursor.fetchone()

        if res:
            print(f"\n查询结果：学号 {res[1]} 姓名 {res[2]} 年龄 {res[3]} 专业 {res[4]}")
        else:
            print("未找到该学生")

    # 4. 修改学生信息
    def update_student(self, stu_id, new_age, new_major):
        try:
            sql = "UPDATE student1 SET age=%s, major=%s WHERE stu_id=%s"
            self.cursor.execute(sql, (new_age, new_major, stu_id))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("✅ 修改成功")
                self.write_log(f"修改学生：{stu_id}")
            else:
                print("未找到该学生")
        except:
            self.conn.rollback()
            print("❌ 修改失败")

    # 5. 删除学生
    def delete_student(self, stu_id):
        try:
            sql = "DELETE FROM student1 WHERE stu_id=%s"
            self.cursor.execute(sql, stu_id)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("✅ 删除成功")
                self.write_log(f"删除学生：{stu_id}")
            else:
                print("未找到该学生")
        except:
            self.conn.rollback()
            print("❌ 删除失败")

    def close(self):
        self.cursor.close()
        self.conn.close()

# ===================== 登录界面 =====================
def login_system(sm):
    print("======= 管理员登录 =======")
    for i in range(3):
        username = input("请输入账号：")
        password = input("请输入密码：")

        if sm.admin_login(username, password):
            print("✅ 登录成功！")
            return True
        else:
            print(f"❌ 账号或密码错误，剩余次数：{2-i}")
    print("🔴 登录失败，程序退出")
    return False

# ===================== 主菜单 =====================
def main():
    sm = StudentManager()
    if not login_system(sm):
        return

    while True:
        print("\n======= 学生信息管理系统 =======")
        print("1. 添加学生")
        print("2. 查看所有学生")
        print("3. 按学号查询学生")
        print("4. 修改学生信息")
        print("5. 删除学生")
        print("0. 退出系统")

        choice = input("请输入功能编号：")

        if choice == "1":
            sid = input("请输入学号：")
            name = input("请输入姓名：")
            age = input("请输入年龄：")
            major = input("请输入专业：")
            sm.add_student(sid, name, age, major)

        elif choice == "2":
            sm.show_all()

        elif choice == "3":
            sid = input("请输入要查询的学号：")
            sm.search_by_id(sid)

        elif choice == "4":
            sid = input("请输入要修改的学号：")
            age = input("请输入新年龄：")
            major = input("请输入新专业：")
            sm.update_student(sid, age, major)

        elif choice == "5":
            sid = input("请输入要删除的学号：")
            sm.delete_student(sid)

        elif choice == "0":
            sm.close()
            print("系统已退出")
            break
        else:
            print("输入无效，请输入 0-5 之间的数字")

if __name__ == "__main__":
    main()