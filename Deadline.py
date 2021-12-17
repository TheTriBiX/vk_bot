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
            a = """SELECT * FROM deadline WHERE subject IN ('аип')"""
        elif deadline_aip == 'асис':
            a = """SELECT * FROM deadline WHERE subject IN ('асис')"""
        elif deadline_aip == 'инфа':
            a = """SELECT * FROM deadline WHERE subject IN ('инфа')"""
        elif deadline_aip == 'матан':
            a = """SELECT * FROM deadline WHERE subject IN ('матан')"""
        else:
            a = """SELECT * FROM deadline"""
        cur.execute(a)
        return cur


def edit_deadline(stage, user_id, msg):
    with sq.connect("users.db") as db:
        cur = db.cursor()
        if stage == 4:
            cur.execute("""INSERT INTO deadline (subject, type, date) VALUES (?, ?, ?)""",
                        (msg))
        elif stage == 5:
            cur.execute("""INSERT INTO deadline (subject, type, date, description) VALUES (?, ?, ?, ?)""",
                        (msg))

