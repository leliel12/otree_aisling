from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):

    form_model = models.Player
    form_fields = ["computer", "gender"]

class BigFive(Page):

    form_model = models.Player
    form_fields = [
        'is_talkative',
        'tends_to_find_fault_with_others',

        'does_a_thorough_job',
        'is_depressed_blue',
        'is_original_comes_up_with_new_ideas',

        'has_an_active_imagination',
        'tends_to_be_quiet',
        'is_generally_trusting',

        'tends_to_be_lazy',
        'is_emotionally_stable_not_easily_upset',
    ]


page_sequence = [
    Intro, BigFive
]
