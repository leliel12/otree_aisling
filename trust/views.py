#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class AsignmentPage(WaitPage):

    title_text = "Groups Assignments"
    body_text = "Waiting for all groups to reasign players"
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def group(self, subsession):
        by_ttype = {k: [] for k in Constants.ttypes}
        for player in subsession.get_players():
            player.trust_type = player.participant.vars["trust_type"]
            by_ttype[player.trust_type].append(player)

        map(random.shuffle, by_ttype.values())
        # match players
        matched = zip(*by_ttype.values())

        mtx = []
        for p1, p2 in matched:
            if random.choice([True, False]):
                p1, p2 = p2, p1
            mtx.append([p1, p2])
        subsession.set_group_matrix(mtx)

    def after_all_players_arrive(self):
        for subsession in self.subsession.in_rounds(1, Constants.num_rounds):
            self.group(subsession)


class Instructions(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Expect(Page):

    form_model = models.Player
    form_fields = ["expect_other_player_to_return",
                   "expect_other_player_to_return_revealed"]

    def is_displayed(self):
        return self.player.role() == Constants.sender

    def vars_for_template(self):
        returner = self.group.get_player_by_role(Constants.returner)
        return {"returner": returner}


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
