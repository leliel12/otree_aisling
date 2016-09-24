from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Question(Page):

    form_model = models.Player
    form_fields = ["ammount_given"]


class TrustTypeWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_ttype()


class Results(Page):

    def vars_for_template(self):
        return {"keept": Constants.allocated_amount - self.player.ammount_given,
                "give": self.player.ammount_given * 3}


page_sequence = [
    #~ Introduction,
    Question, TrustTypeWaitPage, Results
]
