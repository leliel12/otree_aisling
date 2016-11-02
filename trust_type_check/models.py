
import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Your name here'

doc = """
This app determine your trustworty
"""


class Constants(BaseConstants):
    name_in_url = 'tt_checker'
    players_per_group = None
    num_rounds = 1
    allocated_amount = c(10)

    ttype_trustworthy = "Trustworthy"
    ttype_not_trustworthy = "Not trustworthy"
    ttypes = (ttype_trustworthy, ttype_not_trustworthy)


class Subsession(BaseSubsession):

    def set_ttype(self):
        def get_ammount(player):
            return (
                player.ammount_given +
                player.trust_scenario_you_are_A +
                player.trust_scenario_you_are_B)

        players = [(get_ammount(p), random.random(), p)
                   for p in self.get_players()]
        half = int(round(len(players) / 2))
        by_trust = [p[-1] for p in sorted(players)]
        for idx, player in enumerate(by_trust):
            player.trust_type = (
                Constants.ttype_not_trustworthy
                if idx < half else
                Constants.ttype_trustworthy)
            player.participant.vars["trust_type"] = player.trust_type

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    ammount_given = models.CurrencyField(
        doc="""Amount dictator decided to give to the other player""",
        min=0, max=Constants.allocated_amount, widget=widgets.SliderInput(),
        verbose_name='I will give (from 0 to %i)' % Constants.allocated_amount)

    trust_scenario_you_are_A = models.CurrencyField(
            min=0, max=10, widget=widgets.SliderInput(attrs={'step': '1'}),
            verbose_name='I will give (from 0 to 10)')
    trust_scenario_you_are_B = models.CurrencyField(
            min=0, max=30, widget=widgets.SliderInput(attrs={'step': '1'}),
            verbose_name='I will give (from 0 to 30)')


    trust_type = models.CharField(max_length=20, choices=Constants.ttypes)
