from datetime import datetime

import smokesignal

from creatures import Player
from items import Gold
from score import Score
from globals import EVENT_MONSTER_DEAD, EVENT_DAMAGE_RECIEVED, EVENT_BOTTLE_USED, EVENT_DAMAGE_GIVEN, \
    EVENT_ITEM_ASSIGNED, EVENT_TRIGGER_RUN


class DefaultHandler:
    def __init__(self):
        self.__recievers = []

    def _register(self, signals, callback):
        self.__recievers.append(smokesignal.on(signals, callback))

    def clean(self):
        for i in self.__recievers:
            smokesignal.disconnect(i)


class DeathHandler(DefaultHandler):
    def __init__(self, game):
        super().__init__()
        self.__game = game
        self._register(EVENT_MONSTER_DEAD, self.__monster_dead)

    def __monster_dead(self, creature):
        if type(creature).__name__ == Player.__name__:
            self.__game.death_delayed()


class TriggerHandler(DefaultHandler):
    def __init__(self, trigger_name, key_name, game):
        super().__init__()
        self.__game = game
        self.__trigger_name = trigger_name
        self.__key_name = key_name
        self._register(EVENT_TRIGGER_RUN, self._trigger_run)

    def _trigger_run(self, trigger, key):
        print(type(self).__name__, "handled", type(trigger).__name__, "run by", type(key).__name__)

    def _get_game(self):
        return self.__game

    def _get_trigger_name(self):
        return self.__trigger_name

    def _get_key_name(self):
        return self.__key_name


class NextLevelHandler(TriggerHandler):
    def _trigger_run(self, trigger, key):
        super()._trigger_run(trigger, key)
        if type(trigger).__name__ == self._get_trigger_name() and type(key).__name__ == self._get_key_name():
            self._get_game().next_level_delayed()


class OpenChestHandler(TriggerHandler):
    def _trigger_run(self, trigger, key):
        super()._trigger_run(trigger, key)
        if type(trigger).__name__ == self._get_trigger_name() and type(key).__name__ == self._get_key_name():
            trigger.set_lootable(True)


class DisappearHandler(TriggerHandler):
    def _trigger_run(self, trigger, key):
        super()._trigger_run(trigger, key)
        if type(trigger).__name__ == self._get_trigger_name() and type(key).__name__ == self._get_key_name():
            trigger.kill()


class MoveToHandler(TriggerHandler):
    def __init__(self, trigger_name, key_name, x, y, game):
        super().__init__(trigger_name, key_name, game)
        self.__pos = (x, y)

    def _trigger_run(self, trigger, key):
        super()._trigger_run(trigger, key)
        if type(trigger).__name__ == self._get_trigger_name() and type(key).__name__ == self._get_key_name():
            self._get_game().get_player().set_position(*self.__pos)


class ScoreHandler(DefaultHandler):
    def __init__(self, level, game_id):
        super().__init__()
        self.__gold = dict()
        self.__score = Score(level=level, game_id=game_id, time_start=datetime.now())
        Score.add(self.__score)
        self._register(EVENT_MONSTER_DEAD, self.__monster_dead)
        self._register(EVENT_DAMAGE_RECIEVED, self.__damage_recieved)
        self._register(EVENT_DAMAGE_GIVEN, self.__damage_given)
        self._register(EVENT_BOTTLE_USED, self.__bottle_used)
        self._register(EVENT_ITEM_ASSIGNED, self.__item_assigned)

    def __monster_dead(self, creature):
        print(type(creature).__name__, "is dead")
        if type(creature).__name__ != Player.__name__:
            self.__score.kills += 1
            Score.add(self.__score)

    def __damage_recieved(self, actor, damage, clean_damage):
        print(type(actor).__name__, "is attacked with", damage, "damage but recieved", clean_damage)
        if type(actor).__name__ == Player.__name__:
            self.__score.damage_absorbed += damage - clean_damage
            self.__score.damage_recieved += clean_damage
            Score.add(self.__score)

    def __damage_given(self, actor, enemy, weapon, damage):
        print(type(actor).__name__, "attacked", type(enemy).__name__, "using", type(weapon).__name__, "with", damage,
              "damage")
        if type(actor).__name__ == Player.__name__:
            self.__score.damage_given += damage
            Score.add(self.__score)

    def __bottle_used(self, _, creature, bottle):
        print(type(creature).__name__, "used a bottle", type(bottle).__name__)
        if type(creature).__name__ == Player.__name__:
            self.__score.bottles_used += 1
            Score.add(self.__score)

    def __item_assigned(self, actor, slot, item):
        count = 0
        if item:
            count = item.get_count()
        print(type(actor).__name__, f"put into the slot[{slot}]", count, type(item).__name__)
        if type(actor).__name__ == Player.__name__:
            if type(item).__name__ == Gold.__name__:
                self.__gold[slot] = count
            else:
                self.__gold[slot] = 0
            self.__score.gold = sum(self.__gold.values())
            Score.add(self.__score)
