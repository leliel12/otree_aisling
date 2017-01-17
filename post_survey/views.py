from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class PostSurvey(Page):

    form_model = models.Player
    form_fields = [
        'extraverted_enthusiastic',
        'dependable_self_disciplined',
        'open_new_speriences',
        'sympathetic_warm',
        'calm_emotionally_stable',
        'critical_quarrelsome',
        'anxious_easily_upset',
        'reserved_quiet',
        'disorganized_careless',
        'conventional_uncreative',

        'asian',
        'black_african_american',
        'hispanic_latino',
        'white',
        'other',
        'prefer_not_to_state',

        "major",
        "year_berkeley",
        "stem_courses",
        "economic_courses",
        "gender",
    ]

class Finish(Page):
    pass


page_sequence = [
    PostSurvey, Finish
]


