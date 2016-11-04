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
        "auto_type": self.session.config.get("auto_ttype")}


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
        trustworthy = [
            p for p in participants
            if p.vars["trust_type"] == Constants.ttype_trustworthy]
        not_trustworthy = [
            p for p in participants
            if p.vars["trust_type"] == Constants.ttype_not_trustworthy]

        group_candidates = (
            self._get_group_candidates(trustworthy, not_trustworthy)
            if self.subsession.treatment_trustworthy_first else
            self._get_group_candidates(not_trustworthy, trustworthy))

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


    def get_form_fields(self):
        fields = ["expect_other_player_to_return"]
        if self.subsession.treatment_reveal_type:
            fields.append("expect_other_player_to_return_revealed")
        return fields

    form_fields = ["expect_other_player_to_return",
                   "expect_other_player_to_return_revealed"]

    def is_displayed(self):
        return self.player.role() == Constants.sender

    def vars_for_template(self):
        returner = self.group.get_player_by_role(Constants.returner)
        reveal = self.subsession.treatment_reveal_type
        return {"returner": returner, "reveal": reveal}


class Offer(Page):

    form_model = models.Group
    form_fields = ["ammount_given"]

    def is_displayed(self):
        return self.player.role() == Constants.sender


class OfferWaitPage(WaitPage):
    title_text = "Waiting for the sender"
    body_text = "Waiting for the sender"


class Return(Page):

    form_model = models.Group
    form_fields = ["ammount_sent_back"]

    def is_displayed(self):
        return self.player.role() == Constants.returner

    def vars_for_template(self):
        return {"return_max": int(self.group.ammount_given * 3)}


class ReturnWaitPage(WaitPage):
    title_text = "Waiting for the returner"
    body_text = "Waiting for the returner"


class Results(Page):

    def vars_for_template(self):
        return {"return_max": int(self.group.ammount_given * 3)}



page_sequence = [
    AsignmentPage,
    Instructions,
    Expect,
    Offer, OfferWaitPage,
    Return, ReturnWaitPage,
    Results
]
