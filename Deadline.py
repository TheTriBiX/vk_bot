import sqlite3 as sq
def deadline(deadline_aip):
    with sq.connect("users.db") as db:
        cur = db.cursor() #курсор

        cur.execute("""CREATE TABLE IF NOT EXISTS deadline (
            subject STRING NOT NULL, 
            type STRING NOT NULL, 
            date STRING NOT NULL, 
            description TEXT)
            """)
        if deadline_aip == 'аип':
            a = """SELECT * FROM deadline WHERE subject IN ('АиП')"""
        elif deadline_aip == 'асис':
            a = """SELECT * FROM deadline WHERE subject IN ('АСиС')"""
        elif deadline_aip == 'инфа':
            a = """SELECT * FROM deadline WHERE subject IN ('Информатика')"""
        elif deadline_aip == 'матан':
            a = """SELECT * FROM deadline WHERE subject IN ('Математический анализ')"""
        else:
            a = """SELECT * FROM deadline"""

        cur.execute(a)
        #for res in cur:
        #    print(res)
        return cur

