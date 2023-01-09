import smokesignal

from creatures import Player
from score import Score
from settings import EVENT_MONSTER_DEAD, EVENT_DAMAGE_RECIEVED, EVENT_BOTTLE_USED, EVENT_DAMAGE_GIVEN, \
    EVENT_ITEM_ASSIGNED


class Scenario:
    def __init__(self):
        self.complete = False

    def mark_done(self):
        self.complete = True

    def is_complete(self):
        return self.complete


class ScenarioLevel1(Scenario):
    pass


class ScoreHandler:
    def __init__(self, level):
        self.score = Score(level=level)
        Score.add(self.score)
        smokesignal.on(EVENT_MONSTER_DEAD, self.monster_dead)
        smokesignal.on(EVENT_DAMAGE_RECIEVED, self.damage_recieved)
        smokesignal.on(EVENT_DAMAGE_GIVEN, self.damage_given)
        smokesignal.on(EVENT_BOTTLE_USED, self.bottle_used)
        smokesignal.on(EVENT_ITEM_ASSIGNED, self.item_assigned)

    def monster_dead(self, actor):
        print("Monster killed", actor)
        if actor != Player.__name__:
            self.score.kills += 1
            Score.add(self.score)

    def damage_recieved(self, actor, damage, clean_damage):
        print("Damage recieved", actor, damage, clean_damage)
        if actor == Player.__name__:
            self.score.damage_absorbed += damage - clean_damage
            self.score.damage_recieved += clean_damage
            Score.add(self.score)

    def damage_given(self, actor, weapon, damage):
        print(actor, "Damage given", weapon, damage)
        if actor == Player.__name__:
            self.score.damage_given += damage
            Score.add(self.score)

    def bottle_used(self, actor, bottle, heal):
        print("Bottle used", actor, bottle, heal)
        if actor == Player.__name__:
            self.score.bottles_used += 1
            Score.add(self.score)

    def item_assigned(self, actor, item, count):
        # TODO make gold calculation
        pass
