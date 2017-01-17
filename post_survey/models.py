from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'post_survey'
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

    extraverted_enthusiastic = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Extraverted, enthusiastic")
    dependable_self_disciplined = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Dependable, self-disciplined")
    open_new_speriences = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Open to new experiences, complex")
    sympathetic_warm = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Sympathetic, warm")
    calm_emotionally_stable = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Calm, emotionally stable")
    critical_quarrelsome = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Critical, quarrelsome")
    anxious_easily_upset = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Anxious, easily upset")
    reserved_quiet = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Reserved, quiet")
    disorganized_careless = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Disorganized, careless")
    conventional_uncreative = models.PositiveIntegerField(
        choices=Constants.agree_levels,
        verbose_name="Conventional, uncreative")


    asian = models.BooleanField(verbose_name="Asian", widget=widgets.CheckboxInput)
    black_african_american = models.BooleanField(verbose_name="Black / African American", widget=widgets.CheckboxInput)
    hispanic_latino = models.BooleanField(verbose_name="Hispanic / Latino", widget=widgets.CheckboxInput)
    white = models.BooleanField(verbose_name="White", widget=widgets.CheckboxInput)
    other = models.BooleanField(verbose_name="Other", widget=widgets.CheckboxInput)
    prefer_not_to_state = models.BooleanField(verbose_name="Prefer not to state", widget=widgets.CheckboxInput)

    major = models.CharField(
        max_length=255, verbose_name="What is your major?")

    year_berkeley = models.PositiveIntegerField(
        widget=widgets.RadioSelectHorizontal,
        choices=list(sorted({1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}.items())),
        verbose_name="What year are you at UC Berkeley?")

    stem_courses = models.PositiveIntegerField(
        verbose_name="How many Science, Technology, Engineering, and Math (STEM) Courses have you taken in university?")

    economic_courses = models.PositiveIntegerField(
        verbose_name="How many economics courses have you taken in university?")

    gender = models.CharField(
        max_length=6, choices=["Male", "Female"],
        widget=widgets.RadioSelectHorizontal,
        verbose_name="What is your gender?")
