
import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'triple_dictator'
    players_per_group = None
    num_rounds = 1
    allocated_amount = c(10)

    ttype_trustworthy = "Trustworthy"
    ttype_not_trustworthy = "Not trustworthy"
    ttypes = (ttype_trustworthy, ttype_not_trustworthy)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def set_ttype(self):
        players = [(p.ammount_given, random.random(), p)
                   for p in self.get_players()]
        half = int(round(len(players) / 2))
        by_trust = [p[-1] for p in sorted(players)]
        for idx, player in enumerate(by_trust):
            player.trust_type = (
                Constants.ttype_not_trustworthy
                if idx < half else
                Constants.ttype_trustworthy)
            player.participant.vars["trust_type"] = player.trust_type


class Player(BasePlayer):

    ammount_given = models.CurrencyField(
        doc="""Amount dictator decided to give to the other player""",
        min=0, max=Constants.allocated_amount, widget=widgets.SliderInput(),
        verbose_name='I will give (from 0 to %i)' % Constants.allocated_amount)
    trust_type = models.CharField(max_length=20, choices=Constants.ttypes)
