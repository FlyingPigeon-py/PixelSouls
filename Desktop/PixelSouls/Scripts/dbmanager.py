import sqlite3


class Manager:
    def __init__(self, db_name):
        self.db_name = db_name

    def set_convert(self, score):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""UPDATE GameStats
        SET BestScore = ?""", (score,))
        con.commit()
        con.close()

    def get_convert(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute('''SELECT BestScore FROM GameStats''').fetchall()
        con.close()
        return result
    
    def set_vol(self, persent):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""UPDATE GameStats
        SET Volume = ?""", (persent,))
        con.commit()
        con.close()

    def get_vol(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute('''SELECT Volume FROM GameStats''').fetchall()
        con.close()
        return result