#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)

from django.core.exceptions import ImproperlyConfigured


from trust_type_check.models import Constants as TTCConstants
from pre_survey.models import Constants as PSConstants

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 10
    half_rounds = int(num_rounds/2)

    amount_allocated = c(10)

    sender = "Sender"
    returner = "Returner"

    trust_scores = {"ttype": (TTCConstants.ttypes, "trust_type"),
                    "pss": (PSConstants.psscores, "ps_score")}

    test_of_understanding = [
        (
            "You are Player A and you just sent over $10 of the $10 you have to player B, how much will player B receive?",
            "3*10=$30",
            "Remember that Player B gets triple the amount you send so in this case you multiply the 10 dollars you send by 3 and get $30."),
        (
            "You are Player B and Player A just decided to give you $5. How much will you actually receive?",
            "3*5 = $15",
            "Remember that Player B always receives triple the amount that Player A decides to send over. So in this case, you will receive 3*5 which is 15 dollars in total."),
        (
            "Player A gives Player B $6 and Player B returns $6. How much are their payoffs?",
            "Player A=$10\nPlayer B=$12",
            "Remember Player A gets to keep anything not sent to Player B")]

    test_of_understanding_percentage = [
        (
            "As Player A, you give $10 to Player B. You expect that player B will return $5 to you. What is the expected percentage of return?",
            "(5/10) *100 = 50%",
            "You sent over $10 and you expected $5-- half of the amount to be returned-that is a 50% rate of return."),
        (
            "After receiving the $10 which turns in $30, Player B decides that they will send back $10. What is the percentage of return from Player B?",
            "(10/10)*100 = 100%",
            "You sent over $10 and received $10 in return. This is a 100% return."),

        (
            "Suppose Player B decides they will send back 200% of whatever Player A sends to them. Then Player A sends $10 which turns into $30. How much money in dollars does Player B return?",
            "($10 * 2.00)= $20",
            "Player B agreed to send 200% and 200% of $10 is $20.")]

    reveal_variation = ("reveal", "no-reveal")
    order_variation = ("first_above", "first_below")
    play_variation = ("simultaneous_first", "sequential_first")



class Subsession(BaseSubsession):

    reveal_variation = models.CharField(max_length=100, choices=Constants.reveal_variation)
    order_variation = models.CharField(max_length=100, choices=Constants.order_variation)
    play_variation = models.CharField(max_length=100, choices=Constants.play_variation)

    round_play_type = models.CharField(max_length=100, choices=Constants.reveal_variation)

    def _check(self, part, value, options, conf):
        if value not in options:
            options = ", ".join(options)
            msg = "In treatment {}, {} variation part of treatment '{}' must be one of: {}.".format(conf, part, value, options)
            raise ImproperlyConfigured(msg)

    def before_session_starts(self):
        treatment = self.session.config['treatment_type']

        self.reveal_variation, self.play_variation, self.order_variation  = treatment
        self._check("reveal", self.reveal_variation, Constants.reveal_variation, str(treatment))
        self._check("order", self.order_variation, Constants.order_variation, str(treatment))
        self._check("play", self.play_variation, Constants.play_variation, str(treatment))

        for player in self.get_players():
            if self.round_number == 1:
                player.selected_round_for_payoff = random.randint(1, Constants.num_rounds)
            else:
                player.selected_round_for_payoff = player.in_round(1).selected_round_for_payoff
        if self.round_number == 1:
            trust_score = self.session.config["trust_score"]
            if trust_score not in Constants.trust_scores:
                raise ValueError("session 'trust_score' must be one of {}".format(Constants.trust_scores))
            if self.session.config.get("auto_trust_score"):
                scores, var_name = Constants.trust_scores[trust_score]
                scores = itertools.cycle(scores)
                for player in self.get_players():
                    player.participant.vars[var_name] = next(scores)

        firsts_rounds, seconds_rounds = [
            s.split("_", 1)[0] for s in Constants.play_variation]
        if self.play_variation == Constants.play_variation[-1]:
            firsts_rounds, seconds_rounds = seconds_rounds, firsts_rounds
        if self.round_number <= Constants.half_rounds:
            self.round_play_type = firsts_rounds
        else:
            self.round_play_type = seconds_rounds


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

    tunderstanding_1 = models.IntegerField(
        verbose_name=Constants.test_of_understanding[0][0])
    tunderstanding_2 = models.IntegerField(
        verbose_name=Constants.test_of_understanding[1][0])
    tunderstanding_3a = models.IntegerField(
        verbose_name=Constants.test_of_understanding[2][0])
    tunderstanding_3b = models.IntegerField()

    tunderstanding_percentage_1 = models.IntegerField(
        min=0, max=100,
        verbose_name=Constants.test_of_understanding_percentage[0][0])
    tunderstanding_percentage_2 = models.IntegerField(
        min=0, max=100,
        verbose_name=Constants.test_of_understanding_percentage[1][0])
    tunderstanding_percentage_3 = models.IntegerField(
        verbose_name=Constants.test_of_understanding_percentage[2][0])

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

    @property
    def score(self):
        trust_score = self.session.config["trust_score"]
        if trust_score == "pss":
            return self.ps_score
        return self.trust_type
