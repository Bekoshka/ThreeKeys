from datetime import datetime

from db import Connection


class GameScore:
    def __init__(self, id=None, kills=0, damage_given=0, damage_recieved=0, damage_absorbed=0,
                 bottles_used=0, gold=0, time_start=None, score=0):
        self.id = id
        self.time_start = time_start
        self.score = score
        self.kills = kills
        self.damage_given = damage_given
        self.damage_recieved = damage_recieved
        self.damage_absorbed = damage_absorbed
        self.bottles_used = bottles_used
        self.gold = gold

    def __repr__(self):
        return f"<GameScore ({self.id}, {self.time_start}, {self.score})>"

    def __str__(self):
        return f"""|{self.id:4d}|{datetime.fromisoformat(self.time_start).strftime("%Y-%m-%d %H-%M-%S")}|""" + \
               f"""{self.score:6d}|{self.kills:3d}|{self.damage_given:6d}|{self.damage_recieved:6d}|""" + \
               f"""{self.damage_absorbed:6d}|{self.bottles_used:3d}|{self.gold:6d}|"""

    @staticmethod
    def title():
        return f"""|Game|     Start time    |Score |KLS|DAMAGE|DMG_RV|DMG_BL|BTL| GOLD |"""

    @staticmethod
    def get(limit=10):
        out = []
        con = Connection()
        c = con.cursor()
        c.execute("""
            SELECT 
                id,
                kills,
                damage_given,
                damage_recieved,
                damage_absorbed,
                bottles_used,
                gold,
                time_start,
                CASE WHEN (kills * 150 + damage_given - damage_recieved + gold) < 0 
                THEN 0 
                ELSE (kills * 150 + damage_given - damage_recieved + gold) 
                END AS score
            FROM (
                SELECT
                    id,
                    kills,
                    damage_given,
                    damage_recieved,
                    damage_absorbed,
                    bottles_used,
                    (SELECT gold FROM scores WHERE id = max_level_id) AS gold,
                    time_start
                FROM (          
                    SELECT 
                        game_id AS id,
                        SUM(kills) AS kills,
                        SUM(damage_given) AS damage_given,
                        SUM(damage_recieved) AS damage_recieved, 
                        SUM(damage_absorbed) AS damage_absorbed,
                        SUM(bottles_used) AS bottles_used,
                        max(id) as max_level_id,
                        MIN(time_start) AS time_start
                    FROM scores 
                    GROUP BY game_id
                )
            )
            ORDER BY score DESC LIMIT ?
        """, (limit,))

        for i in c.fetchall():
            out.append(GameScore(*i))
        return out