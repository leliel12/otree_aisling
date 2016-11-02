from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class TDIntroduction(Page):
    pass


class TDQuestion(Page):

    form_model = models.Player
    form_fields = ["ammount_given"]


class TDResults(Page):

    def vars_for_template(self):
        return {"keept": Constants.allocated_amount - self.player.ammount_given,
                "give": self.player.ammount_given * 3}


class TGInstructions(Page):
    pass


class TGScenarioA(Page):

    form_model = models.Player
    form_fields = ["trust_scenario_you_are_A"]


class TGScenarioB(Page):

    form_model = models.Player
    form_fields = ["trust_scenario_you_are_B"]


class TrustTypeWaitPage(WaitPage):

    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.subsession.set_ttype()


page_sequence = [
    TDIntroduction, TDQuestion, TDResults,
    TGInstructions, TGScenarioA, TGScenarioB,
    TrustTypeWaitPage
]
