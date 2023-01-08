import smokesignal

from creatures import Player
from score import Score
from settings import EVENT_MONSTER_DEAD, EVENT_DAMAGE_RECIEVED, EVENT_BOTTLE_USED


class Scenario:
    def __init__(self):
        self.complete = False

    def mark_done(self):
        self.complete = True

    def is_complete(self):
        return self.complete


class ScenarioLevel1(Scenario):
    def __init__(self):
        smokesignal.on(EVENT_MONSTER_DEAD, self.monster_dead)
        smokesignal.on(EVENT_DAMAGE_RECIEVED, self.damage_recieved)
        smokesignal.on(EVENT_BOTTLE_USED, self.bottle_used)
        super().__init__()
        self.score = Score()
        Score.add(self.score)

    def monster_dead(self, type):
        print("Monster killed", type)
        if type != Player.__name__:
            self.score.kills += 1
            Score.add(self.score)

    def damage_recieved(self, type, damage, clean_damage):
        print("Damage recieved", type, damage, clean_damage)
        if type == Player.__name__:
            self.score.damage_absorbed += damage - clean_damage
            self.score.damage_recieved += clean_damage
        else:
            self.score.damage_given += clean_damage
        Score.add(self.score)

    def bottle_used(self, type, bottle, heal):
        print("Bottle used", type, bottle, heal)
        if type == Player.__name__:
            self.score.bottles_used += 1
            Score.add(self.score)
