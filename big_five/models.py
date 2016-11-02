from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'big_five'
    players_per_group = None
    num_rounds = 1
    agree_level_desc = {
        1: "Disagree Strongly",
        2: "Disagree a little",
        3: "Neither agree nor disagree",
        4: "Agree a little",
        5: "Agree Strongly",
    }
    agree_levels = sorted(agree_level_desc.items())


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    computer = models.CharField(
        max_length=10,
        verbose_name="What computer are you sitting at?")
    gender = models.CharField(
        max_length=6, choices=["Male", "Female"],
        widget=widgets.RadioSelectHorizontal,
        verbose_name="What is your gender?")

    is_talkative = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Extraverted, enthusiastic")
    has_an_active_imagination = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Critical, quarrelsome")
    tends_to_find_fault_with_others = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Dependable, self-disciplined")
    tends_to_be_quiet = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Anxious, easily upset")
    does_a_thorough_job = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Open to new experiences, complex")
    is_generally_trusting = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Reserved, quiet")
    is_depressed_blue = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Sympathetic, warm")
    tends_to_be_lazy = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Disorganized, careless")
    is_original_comes_up_with_new_ideas = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Calm, emotionally stable")
    is_emotionally_stable_not_easily_upset = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Conventional, uncreative")
