import os
import sqlite3

from settings import DATA_DIR
import datetime

DB_FILE = "db.sqlite"


class Connection:
    def __init__(self, debug=False):
        self.con = sqlite3.connect(os.path.join(DATA_DIR, DB_FILE))
        self.con.cursor().execute("PRAGMA foreign_keys = on")
        if debug:
            self.con.set_trace_callback(print)

    def cursor(self):
        return self.con.cursor()

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()


class Score:
    def __init__(self, id=None, level=0, kills=0, damage_given=0, damage_recieved=0, damage_absorbed=0,
                 bottles_used=0, gold=0, time_start=datetime.datetime.now(), total_time=None):
        self.id = id
        self.level = level
        self.kills = kills
        self.damage_given = damage_given
        self.damage_recieved = damage_recieved
        self.damage_absorbed = damage_absorbed
        self.bottles_used = bottles_used
        self.gold = gold
        self.time_start = time_start
        self.total_time = total_time

    def __repr__(self):
        return f"Score {self.id}"

    @staticmethod
    def init_db():
        con = Connection()
        c = con.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER NOT NULL,
            kills INTEGER NOT NULL,
            damage_given INTEGER NOT NULL,
            damage_recieved INTEGER NOT NULL,
            damage_absorbed INTEGER NOT NULL,
            bottles_used INTEGER NOT NULL,
            gold INTEGER NOT NULL,
            time_start DATETIME NOT NULL,
            total_time DATETIME
            )""")

    @staticmethod
    def get():
        out = []
        con = Connection()
        c = con.cursor()
        c.execute("""SELECT id, level, kills, damage_given, damage_recieved, damage_absorbed, bottles_used,
        gold, time_start, total_time FROM scores ORDER BY id ASC""")

        for i in c.fetchall():
            out.append(Score(*i))
        return out

    @staticmethod
    def get_by_id(id):
        out = None
        con = Connection()
        c = con.cursor()
        c.execute("SELECT id, level, kills, damage_given, damage_recieved, damage_absorbed, bottles_used, gold, time_start, total_time "
                  "FROM scores WHERE id = ? ORDER BY id", (id,))

        res = c.fetchall()
        if len(res):
            out = Score(*res[0])
        return out

    @staticmethod
    def add(score, con=None):
        if con is None:
            con = Connection()
            auto_commit = True
        else:
            auto_commit = False
        c = con.cursor()
        if score.id is None:
            c.execute(
                'INSERT INTO scores (level, kills, damage_given, damage_recieved, damage_absorbed, bottles_used, gold, '
                'time_start, total_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id',
                (score.level, score.kills, score.damage_given, score.damage_recieved, score.damage_absorbed,
                 score.bottles_used, score.gold, score.time_start, score.total_time))
            r = c.fetchone()
            score.id = r[0]
        else:
            c.execute("""UPDATE scores
                                    SET level = ?, kills = ?, damage_given = ?, damage_recieved = ?, 
                                    damage_absorbed = ?, bottles_used = ?, gold = ?, time_start = ?, total_time = ?
                                    WHERE id = ?
                                    """,
                      (score.level, score.kills, score.damage_given, score.damage_recieved, score.damage_absorbed,
                       score.bottles_used, score.gold, score.time_start, score.total_time, score.id))
        if auto_commit:
            con.commit()

    @staticmethod
    def remove(score, con=None):
        if con is None:
            con = Connection()
            auto_commit = True
        else:
            auto_commit = False
        c = con.cursor()
        c.execute("DELETE FROM scores WHERE id=?", (score.id,))
        if auto_commit:
            con.commit()


Score.init_db()

