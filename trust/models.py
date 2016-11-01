#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)

from triple_dictator.models import Constants as TDConstants

author = 'Your name here'

doc = """
Your app description
"""


class Constants(TDConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 2

    amount_allocated = c(10)

    sender = "Sender"
    returner = "Returner"


class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1 and self.session.config.get("auto_ttype"):
            ttypes = itertools.cycle(Constants.ttypes)
            for player in self.get_players():
                player.participant.vars["trust_type"] = next(ttypes)


class Group(BaseGroup):

    ammount_given = models.CurrencyField(
        doc="""Amount the sender decided to give to the other player""",
        min=0, max=Constants.amount_allocated , widget=widgets.SliderInput(),
        verbose_name='I will give (from 0 to %i)' % Constants.amount_allocated)

    ammount_sent_back = models.CurrencyField(
        doc="""Amount the returner decided to sent_back to the other player""",
        min=0, widget=widgets.SliderInput())


class Player(BasePlayer):

    expect_other_player_to_return = models.IntegerField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=300, widget=widgets.SliderInput(),
        verbose_name='What percentage do you think the other will return? (from 0 to 300%)')

    expect_other_player_to_return_revealed = models.IntegerField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=300, widget=widgets.SliderInput(),
        verbose_name='What percentage do you think the other will return? (from 0 to 300%)')

    def role(self):
        return {1: Constants.sender, 2: Constants.returner}[self.id_in_group]

    @property
    def trust_type(self):
        return self.participant.vars["trust_type"]
