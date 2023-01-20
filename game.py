from db import Connection


class Game:
    def __init__(self, id=None):
        self.id = id

    def __repr__(self):
        return f"<Game ({self.id})>"

    @staticmethod
    def init_db():
        con = Connection()
        c = con.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT
            )""")

    @staticmethod
    def get():
        out = []
        con = Connection()
        c = con.cursor()
        c.execute("""SELECT id FROM games ORDER BY id ASC""")

        for i in c.fetchall():
            out.append(Game(*i))
        return out

    @staticmethod
    def get_by_id(id):
        out = None
        con = Connection()
        c = con.cursor()
        c.execute("SELECT id FROM games WHERE id = ?", (id,))

        res = c.fetchall()
        if len(res):
            out = Game(*res[0])
        return out

    @staticmethod
    def add(game, con=None):
        if con is None:
            con = Connection()
            auto_commit = True
        else:
            auto_commit = False
        c = con.cursor()
        if game.id is None:
            c.execute('INSERT INTO games (id) VALUES (NULL) RETURNING id')
            r = c.fetchone()
            game.id = r[0]
        if auto_commit:
            con.commit()

    @staticmethod
    def remove(game, con=None):
        if con is None:
            con = Connection()
            auto_commit = True
        else:
            auto_commit = False
        c = con.cursor()
        c.execute("DELETE FROM games WHERE id=?", (game.id,))
        if auto_commit:
            con.commit()


Game.init_db()
