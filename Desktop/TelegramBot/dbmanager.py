import sqlite3


class Manager:
    def __init__(self, db_name):
        self.db_name = db_name

    def add_user(self, id, name):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""INSERT INTO Users(id,name,diff) VALUES(?,?,?)""", (id, name, 1))
        con.commit()
        con.close()

    def get_user(self, id):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute(
            f'''SELECT id, name, diff, current_exemple, current_answer FROM Users WHERE id = {id}''').fetchall()
        con.close()
        return result

    def get_users(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute('''SELECT id, name, diff, current_exemple, current_answer FROM Users''').fetchall()
        con.close()
        return result

    def user_set_exemple(self, id, exemple):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"""UPDATE Users
        SET current_exemple = "{exemple}" WHERE id = {id}""")
        con.commit()
        con.close()

    def user_set_answer(self, id, answer):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"""UPDATE Users SET current_answer = "{answer}" WHERE id = {id}""")
        con.commit()
        con.close()

    def user_set_difficult(self, id, diff):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"""UPDATE Users SET diff = {diff} WHERE id = {id}""")
        con.commit()
        con.close()

    def get_image(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute('''SELECT id, answer FROM Image''').fetchall()
        con.close()
        return result

    def get_text(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute('''SELECT id, answer FROM Text''').fetchall()
        con.close()
        return result
