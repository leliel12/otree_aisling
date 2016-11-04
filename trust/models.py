#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)

from trust_type_check.models import Constants as TTCConstants

author = 'Your name here'

doc = """
Your app description
"""


class Constants(TTCConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 2

    amount_allocated = c(10)

    sender = "Sender"
    returner = "Returner"


class Subsession(BaseSubsession):

    treatment_reveal_type = models.BooleanField()
    treatment_trustworthy_first = models.BooleanField()

    def before_session_starts(self):
        self.treatment_reveal_type = self.session.config['treatment_reveal_type']
        self.treatment_trustworthy_first = self.session.config['treatment_trustworthy_first']

        for player in self.get_players():
            if self.round_number == 1:
                player.selected_round_for_payoff = random.randint(1, Constants.num_rounds)
            else:
                player.selected_round_for_payoff = player.in_round(1).selected_round_for_payoff

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

    @property
    def sender_payoff(self):
        return Constants.amount_allocated - self.ammount_given + self.ammount_sent_back

    @property
    def returner_payoff(self):
        return (self.ammount_given * 3) - self.ammount_sent_back

    def set_payoff(self):
        for player in self.get_players():
            selected_round = player.selected_round_for_payoff
            player_of_selected_round = player.in_round(selected_round)
            group_of_selected_round = player_of_selected_round.group
            if player_of_selected_round.role() == Constants.sender:
                player.payoff = group_of_selected_round.sender_payoff
            else:
                player.payoff = group_of_selected_round.returner_payoff


class Player(BasePlayer):

    expect_other_player_to_return = models.IntegerField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=300, widget=widgets.SliderInput(),
        verbose_name='What percentage do you think the other will return? (from 0 to 300%)')

    expect_other_player_to_return_revealed = models.IntegerField(
        doc="""What do you expect that the other player will return?""",
        min=0, max=300, widget=widgets.SliderInput(),
        verbose_name='What percentage do you think the other will return? (from 0 to 300%)')

    selected_round_for_payoff = models.PositiveIntegerField()


    def role(self):
        return {1: Constants.sender, 2: Constants.returner}[self.id_in_group]

    @property
    def trust_type(self):
        return self.participant.vars["trust_type"]
