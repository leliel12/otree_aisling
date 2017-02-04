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
        "treatment-conf": self.session.config["treatment_type"],
        "auto_trust_score": self.session.config.get("auto_trust_score"),
        "trust_score": self.session.config["trust_score"],
        "voted_round": self.subsession.voted_round}


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
            list(next(group_candidates)) for _ in range(0, int(num_rounds/4))]
        second_half = [invert_groups(g) for g in first_half]
        total = first_half + second_half + first_half + second_half
        return total

    def _participants_to_players(self, participants, subsession):
        p2p = {p.participant: p for p in subsession.get_players()}
        return [[p2p[p] for p in  g] for g in  participants]

    def after_all_players_arrive(self):
        trust_score = self.session.config["trust_score"]
        scores, var_name = Constants.trust_scores[trust_score]

        group_a, group_b = [], []
        for p in self.subsession.get_players():
            participant = p.participant
            if participant.vars[var_name] == scores[0]:
                group_a.append(participant)
            elif participant.vars[var_name] == scores[1]:
                group_b.append(participant)
            else:
                raise ValueError()
        if self.subsession.order_variation == "first_below":
            group_a, group_b = group_b, group_a

        group_candidates = self._get_group_candidates(group_a, group_b)
        groups = self._select_groups(group_candidates, Constants.normal_game_rounds)
        while len(groups) < Constants.num_rounds:
            groups.append(list(next(group_candidates)))
        for subsession in self.subsession.in_rounds(1, Constants.num_rounds):
            group = groups[subsession.round_number - 1]
            players = self._participants_to_players(group, subsession)
            subsession.set_group_matrix(players)

            # copy the value of round_play_type to every group
            for gobject in subsession.get_groups():
                gobject.group_play_type = subsession.round_play_type


class Instructions(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Expect(Page):

    form_model = models.Player

    def is_displayed(self):
        return self.player.role() == Constants.sender and self.subsession.normal_round

    def get_form_fields(self):
        fields = ["expect_other_player_to_return"]
        if self.subsession.reveal_variation == "reveal":
            fields.append("expect_other_player_to_return_revealed")
        return fields

    def vars_for_template(self):
        trust_score = self.session.config["trust_score"]
        scores, var_name = Constants.trust_scores[trust_score]

        returner = self.group.get_player_by_role(Constants.returner)

        returner_trustworthy = (self.player.score == scores[-1])
        return {"returner": returner, "returner_trustworthy": returner_trustworthy}


class WaitForExpectation(WaitPage):

    def is_displayed(self):
        return self.subsession.normal_round


# =============================================================================
# VOTED ROUNDS
# =============================================================================

class InstructionsVoting(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.first_voted_round


class Voting(Page):
    form_model = models.Player
    form_fields = ["vote_game"]

    def is_displayed(self):
        return self.subsession.voted_round

    def vars_for_template(self):
        trust_score = self.session.config["trust_score"]
        scores, var_name = Constants.trust_scores[trust_score]
        return {
            "player_trustworthy": (self.player.score == scores[0]),
            "partner": self.player.get_others_in_group()[0]}


class WaitVote(WaitPage):

    def is_displayed(self):
        return self.subsession.voted_round

    def after_all_players_arrive(self):
        self.group.choice_group_play_type_by_vote()


class VoteResult(Page):
    def is_displayed(self):
        return self.subsession.voted_round

    def vars_for_template(self):
        selected = self.group.selected_vote
        for k, v in Constants.votes:
            if k == selected:
                return {"scenario": v}


# =============================================================================
# GAME
# =============================================================================

class Offer(Page):

    form_model = models.Group
    form_fields = ["ammount_given"]

    def vars_for_template(self):
        trust_score = self.session.config["trust_score"]
        scores, var_name = Constants.trust_scores[trust_score]

        returner = self.group.get_player_by_role(Constants.returner)

        returner_trustworthy = (self.player.score == scores[-1])
        return {"returner": returner, "returner_trustworthy": returner_trustworthy}

    def is_displayed(self):
        return self.player.role() == Constants.sender


# =============================================================================
# SEQUENTIAL
# =============================================================================

class OfferSequentialWait(WaitPage):

    title_text = "Waiting for the Player A"
    body_text = "You are the Player B in a sequential game. You need to wait until de Player A make the offer"

    def is_displayed(self):
        return (
            self.group.group_play_type == "sequential" and
            self.player.role() == Constants.returner)


class ReturnSequential(Page):

    form_model = models.Group
    form_fields = ["ammount_sent_back"]

    def vars_for_template(self):
        return {"max_value": int(self.group.ammount_given * 3)}

    def is_displayed(self):
        return (
            self.group.group_play_type == "sequential" and
            self.player.role() == Constants.returner)


# =============================================================================
# SIMULTANEOUS
# =============================================================================

class ReturnSimultaneous(Page):

    form_model = models.Group
    form_fields = ["percentage_sent_back"]

    def is_displayed(self):
        return (
            self.group.group_play_type == "simultaneous" and
            self.player.role() == Constants.returner)


# =============================================================================

class ReturnWaitPage(WaitPage):

    def after_all_players_arrive(self):
        if self.group.group_play_type == "simultaneous":
            self.group.set_ammount_sent_back()
        else:
            self.group.set_percentage_sent_back()
        if self.subsession.round_number == Constants.num_rounds:
            self.group.set_payoff()


class Results(Page):

    def vars_for_template(self):
        return {"return_max": int(self.group.ammount_given * 3)}



page_sequence = [
    GamePortionOfExperiment,
    TestOfUderStanding,
    AnswersTestOfUderStanding,

    ExpectationsAndPercentages,
    TestOfUderStandingPercentages,
    AnswersTestOfUderStandingPercentages,

    AsignmentPage,

    Instructions,
    Expect, WaitForExpectation,

    InstructionsVoting,
    Voting, WaitVote, VoteResult,

    Offer,
    OfferSequentialWait,
    ReturnSimultaneous,
    ReturnSequential,

    ReturnWaitPage,
    Results
]
