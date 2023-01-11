import smokesignal

from creatures import Player
from items import Gold
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
        self.gold = dict()
        self.score = Score(level=level)
        Score.add(self.score)
        smokesignal.on(EVENT_MONSTER_DEAD, self.monster_dead)
        smokesignal.on(EVENT_DAMAGE_RECIEVED, self.damage_recieved)
        smokesignal.on(EVENT_DAMAGE_GIVEN, self.damage_given)
        smokesignal.on(EVENT_BOTTLE_USED, self.bottle_used)
        smokesignal.on(EVENT_ITEM_ASSIGNED, self.item_assigned)

    def monster_dead(self, creature):
        print(creature, "is dead")
        if creature != Player.__name__:
            self.score.kills += 1
            Score.add(self.score)

    def damage_recieved(self, actor, damage, clean_damage):
        print(actor, "is attacked with", damage, "damage but recieved", clean_damage)
        if actor == Player.__name__:
            self.score.damage_absorbed += damage - clean_damage
            self.score.damage_recieved += clean_damage
            Score.add(self.score)

    def damage_given(self, actor, enemy, weapon, damage):
        print(actor, "attacked", enemy, "using", weapon, "with", damage, "damage")
        if actor == Player.__name__:
            self.score.damage_given += damage
            Score.add(self.score)

    def bottle_used(self, actor, bottle, heal):
        print(actor, "used bottle", bottle, "that is able to replinish", heal, "health points")
        if actor == Player.__name__:
            self.score.bottles_used += 1
            Score.add(self.score)

    def item_assigned(self, actor, slot, item, count):
        print(actor, f"put into slot[{slot}]", count, item)
        if actor == Player.__name__:
            if item == Gold.__name__:
                self.gold[slot] = count
            else:
                self.gold[slot] = 0
            self.score.gold = sum(self.gold.values())
            Score.add(self.score)
