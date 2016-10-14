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
    num_rounds = 10

    amount_allocated = c(100)

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
        min=0, max=Constants.allocated_amount, widget=widgets.SliderInput(),
        verbose_name='I will give (from 0 to %i)' % Constants.allocated_amount)

    ammount_sent_back = models.CurrencyField(
        doc="""Amount the returner decided to sent_back to the other player""",
        min=0, widget=widgets.SliderInput())


class Player(BasePlayer):

    expect_other_player_to_return = models.CurrencyField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=Constants.allocated_amount*3, widget=widgets.SliderInput(),
        verbose_name='The anoher player will return (from 0 to %i)' % (Constants.allocated_amount * 3))
    trust_type = models.CharField(max_length=20, choices=Constants.ttypes)

    expect_other_player_to_return_revealed = models.CurrencyField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=Constants.allocated_amount*3, widget=widgets.SliderInput(),
        verbose_name='The anoher player will return (from 0 to %i)' % (Constants.allocated_amount * 3))

    def role(self):
        return {1: Constants.sender, 2: Constants.returner}[self.id_in_group]
