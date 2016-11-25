from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'pre_survey'
    players_per_group = None
    num_rounds = 1

    describe_me_level = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    donate_max = 1600



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    people_best_intentions = models.IntegerField(
        choices=Constants.describe_me_level,
        verbose_name="I assume that people have only the best intentions:")
    will_to_return_a_favor = models.IntegerField(
        choices=Constants.describe_me_level,
        verbose_name="When someone does me a favor, I am willing to return it:")
    give_to_without_expecting_anything_in_return = models.IntegerField(
        choices=Constants.describe_me_level,
        verbose_name="I am willing to give to good causes without expecting anything in return:")


    donate = models.IntegerField(min=0, max=Constants.donate_max)

    present = models.IntegerField(
        verbose_name="Which present do you give to the stranger?",
        widget=widgets.RadioSelect(),
        choices=[(0, 'No, would not give present'),
                 (10, 'The present worth 10 U.S. dollars'),
                 (20, 'The present worth 20 U.S. dollars'),
                 (30, 'The present worth 30 U.S. dollars'),
                 (40, 'The present worth 40 U.S. dollars'),
                 (50, 'The present worth 50 U.S. dollars'),
                 (60, 'The present worth 60 U.S. dollars')])

