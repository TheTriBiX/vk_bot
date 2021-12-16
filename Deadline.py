import sqlite3 as sq
def deadline():
    with sq.connect("users.db") as db:
        cur = db.cursor() #курсор

        cur.execute("""CREATE TABLE IF NOT EXISTS deadline (
            subject STRING NOT NULL, 
            type STRING NOT NULL, 
            date STRING NOT NULL, 
            description TEXT)
            """)
        a = """SELECT * FROM deadline """

        n = """SELECT * FROM deadline """
        cur.execute(a)
        #for res in cur:
        #    print(res)
        return cur
