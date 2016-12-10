#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)

from trust_type_check.models import Constants as TTCConstants
from pre_survey.models import Constants as PSConstants

author = 'Your name here'

doc = """
Your app description
"""


class Constants(TTCConstants, PSConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 2

    amount_allocated = c(10)

    sender = "Sender"
    returner = "Returner"

    trust_scores = ("ttype", "pss")


class Subsession(BaseSubsession):

    treatment_reveal_type = models.BooleanField()

    def before_session_starts(self):
        self.treatment_reveal_type = self.session.config['treatment_reveal_type']

        for player in self.get_players():
            if self.round_number == 1:
                player.selected_round_for_payoff = random.randint(1, Constants.num_rounds)
            else:
                player.selected_round_for_payoff = player.in_round(1).selected_round_for_payoff
        if self.round_number == 1:
            trust_score = self.session.config["trust_score"]
            if trust_score not in Constants.trust_scores:
                raise ValueError("session 'trust_score' must be one of {}".format(Constants.trust_scores))
            if trust_score == "ttype" and self.session.config.get("auto_ttype"):
                ttypes = itertools.cycle(Constants.ttypes)
                for player in self.get_players():
                    player.participant.vars["trust_type"] = next(ttypes)
            if trust_score == "pss" and  self.session.config.get("auto_pss"):
                psscores = itertools.cycle(Constants.psscores)
                for player in self.get_players():
                    player.participant.vars["ps_score"] = next(psscores)



class Group(BaseGroup):

    ammount_given = models.CurrencyField(
        doc="""Amount the sender decided to give to the other player""",
        min=0, max=Constants.amount_allocated , widget=widgets.SliderInput(),
        verbose_name='I will give (from 0 to %i)' % Constants.amount_allocated)

    percentage_sent_back = models.PositiveIntegerField(
        verbose_name="Percentage to return (from 0 to 300%)", min=0, max=300,
         widget=widgets.SliderInput())

    ammount_sent_back = models.CurrencyField(
        doc="""Amount the returner decided to sent_back to the other player""")

    @property
    def sender_payoff(self):
        return Constants.amount_allocated - self.ammount_given + self.ammount_sent_back

    @property
    def returner_payoff(self):
        return (self.ammount_given * 3) - self.ammount_sent_back

    def set_ammount_sent_back(self):
        self.ammount_sent_back = (
            self.ammount_given * self.percentage_sent_back / 100.)

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

    @property
    def ps_score(self):
        return self.participant.vars["ps_score"]
