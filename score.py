from db import Connection


class Score:
    def __init__(self, id=None, game_id=None, level="", kills=0, damage_given=0, damage_recieved=0, damage_absorbed=0,
                 bottles_used=0, gold=0, time_start=None):
        self.id = id
        self.game_id = game_id
        self.level = level
        self.kills = kills
        self.damage_given = damage_given
        self.damage_recieved = damage_recieved
        self.damage_absorbed = damage_absorbed
        self.bottles_used = bottles_used
        self.gold = gold
        self.time_start = time_start

    def __repr__(self):
        return f"<Score ({self.id}, {self.time_start}, {self.level})>"

    @staticmethod
    def init_db():
        con = Connection()
        c = con.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            level TEXT NOT NULL,
            kills INTEGER NOT NULL,
            damage_given INTEGER NOT NULL,
            damage_recieved INTEGER NOT NULL,
            damage_absorbed INTEGER NOT NULL,
            bottles_used INTEGER NOT NULL,
            gold INTEGER NOT NULL,
            time_start DATETIME NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games(id)
            )""")

    @staticmethod
    def get():
        out = []
        con = Connection()
        c = con.cursor()
        c.execute("""SELECT id, game_id, level, kills, damage_given, damage_recieved, damage_absorbed, bottles_used,
        gold, time_start FROM scores ORDER BY id ASC""")

        for i in c.fetchall():
            out.append(Score(*i))
        return out

    @staticmethod
    def get_by_id(id):
        out = None
        con = Connection()
        c = con.cursor()
        c.execute("SELECT id, game_id, level, kills, damage_given, damage_recieved, damage_absorbed, bottles_used,"
                  "gold, time_start FROM scores WHERE id = ?", (id,))

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
                'INSERT INTO scores (game_id, level, kills, damage_given, damage_recieved, damage_absorbed,'
                'bottles_used, gold, time_start) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id',
                (score.game_id, score.level, score.kills, score.damage_given, score.damage_recieved,
                 score.damage_absorbed,
                 score.bottles_used, score.gold, score.time_start))
            r = c.fetchone()
            score.id = r[0]
        else:
            c.execute("""UPDATE scores
                                    SET game_id = ?, level = ?, kills = ?, damage_given = ?, damage_recieved = ?, 
                                    damage_absorbed = ?, bottles_used = ?, gold = ?, time_start = ?
                                    WHERE id = ?
                                    """,
                      (score.game_id, score.level, score.kills, score.damage_given, score.damage_recieved,
                       score.damage_absorbed, score.bottles_used, score.gold, score.time_start, score.id))
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
