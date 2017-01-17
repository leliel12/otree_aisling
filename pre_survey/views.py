from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):

    form_model = models.Player
    form_fields = ["computer"]


class Screen1(Page):

    form_model = models.Player
    form_fields = [
        "people_best_intentions",
        "will_to_return_a_favor",
        "give_to_without_expecting_anything_in_return"]


class Screen2(Page):

    form_model = models.Player
    form_fields = ["donate"]


class Screen3(Page):

    form_model = models.Player
    form_fields = ["present"]


class SurveyDebrief(Page):
    pass


class CalculateTrustScore(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_ttype()


page_sequence = [
    Intro,
    Screen1,
    Screen2,
    Screen3,
    SurveyDebrief,
    CalculateTrustScore

]
