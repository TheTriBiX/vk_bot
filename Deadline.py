import sqlite3 as sq


def deadline(deadline_aip):
    """ функция, служащая для нахождения информации по запрашиваемому предмету
    :param deadline_aip: параметр, который указывает на запрашиваемый предмет по которому ищется информация, передаётся
    в виде строки
    :return: отдаёт параметр курсора, который указывает на искомый объект в базе данных
    """
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


def edit_deadline(stage, msg):
    """ функция, которая служит для внесения нового дедлайна в базу данных
    :param stage: указывает на этап в процессе создания информации, принимает в себя цисла от 4 до 5
    :param msg: принимает на вход массив, состоящий либо из 3-х, либо из 4-х строк, которые требуется внести в БД
    """
    with sq.connect("users.db") as db:
        cur = db.cursor()
        if stage == 4:
            cur.execute("""INSERT INTO deadline (subject, type, date) VALUES (?, ?, ?)""",
                        (msg))
        elif stage == 5:
            cur.execute("""INSERT INTO deadline (subject, type, date, description) VALUES (?, ?, ?, ?)""",
                        (msg))
