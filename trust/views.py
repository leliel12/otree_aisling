#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import itertools as it

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {
        "auto_trust_score": self.session.config.get("auto_trust_score"),
        "trust_score": self.session.config["trust_score"]}


# =============================================================================
# PAGES
# =============================================================================

class GamePortionOfExperiment(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class TestOfUderStanding(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ["tunderstanding_1", "tunderstanding_2",
                   "tunderstanding_3a", "tunderstanding_3b"]


class AnswersTestOfUderStanding(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class ExpectationsAndPercentages(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class TestOfUderStandingPercentages(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ["tunderstanding_percentage_1", "tunderstanding_percentage_2",
                   "tunderstanding_percentage_3"]


class AnswersTestOfUderStandingPercentages(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1



class AsignmentPage(WaitPage):

    title_text = "Groups Assignments"
    body_text = "Waiting for all groups to reasign players"
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def _get_group_candidates(self, tw, ntw):
        def shift(seq, n):
            seq = list(seq)
            n = n % len(seq)
            return seq[n:] + seq[:n]
        mtx = [
            shift(it.product([p], ntw), idx) for idx, p in enumerate(tw)]
        mtx_t = list(zip(*mtx))
        random.shuffle(mtx_t)
        return it.cycle(mtx_t)

    def _select_groups(self, group_candidates, num_rounds):
        def invert_groups(groups):
            return [list(reversed(g)) for g in groups]
        first_half = [
            list(next(group_candidates)) for _ in range(0, int(num_rounds/2))]
        second_half = [invert_groups(g) for g in first_half]
        return first_half + second_half

    def _participants_to_players(self, participants, subsession):
        p2p = {p.participant: p for p in subsession.get_players()}
        return [[p2p[p] for p in  g] for g in  participants]

    def after_all_players_arrive(self):
        participants = [p.participant for p in self.subsession.get_players()]

        trust_score = self.session.config["trust_score"]
        scores, var_name = Constants.trust_scores[trust_score]

        grouped = {
            k: list(v)
            for k, v in it.groupby(participants, lambda p:  p.vars[var_name])}

        group_a, group_b = grouped.values()
        group_candidates = self._get_group_candidates(group_a, group_b)
        groups = self._select_groups(group_candidates, Constants.num_rounds)
        for subsession in self.subsession.in_rounds(1, Constants.num_rounds):
            group = groups[subsession.round_number - 1]
            players = self._participants_to_players(group, subsession)
            subsession.set_group_matrix(players)



class Instructions(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Expect(Page):

    form_model = models.Player

    def is_displayed(self):
        return self.player.role() == Constants.sender

    def get_form_fields(self):
        fields = ["expect_other_player_to_return"]
        if self.subsession.treatment_reveal_type:
            fields.append("expect_other_player_to_return_revealed")
        return fields

    def vars_for_template(self):
        returner = self.group.get_player_by_role(Constants.returner)
        reveal = self.subsession.treatment_reveal_type
        return {"returner": returner, "reveal": reveal}


class Offer(Page):

    form_model = models.Group
    form_fields = ["ammount_given"]

    def is_displayed(self):
        return self.player.role() == Constants.sender


class Return(Page):

    form_model = models.Group
    form_fields = ["percentage_sent_back"]

    def is_displayed(self):
        return self.player.role() == Constants.returner


class ReturnWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_ammount_sent_back()
        if self.subsession.round_number == Constants.num_rounds:
            self.group.set_payoff()


class Results(Page):

    def vars_for_template(self):
        return {"return_max": int(self.group.ammount_given * 3)}



page_sequence = [
    GamePortionOfExperiment,
    TestOfUderStanding, AnswersTestOfUderStanding,
    ExpectationsAndPercentages,
    TestOfUderStandingPercentages, AnswersTestOfUderStandingPercentages,

    AsignmentPage,
    Instructions,
    #~ Expect,
    #~ Offer, Return, ReturnWaitPage,
    #~ Results
]
