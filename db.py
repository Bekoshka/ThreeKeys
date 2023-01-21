import os
import sqlite3

from settings import DATA_DIR

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
