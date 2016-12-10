import statistics as stats

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

    presents = {
        0: 'No, would not give present',
        1: 'The present worth 10 U.S. dollars',
        2: 'The present worth 20 U.S. dollars',
        3: 'The present worth 30 U.S. dollars',
        4: 'The present worth 40 U.S. dollars',
        5: 'The present worth 50 U.S. dollars',
        6: 'The present worth 60 U.S. dollars'}

    pss_above = "Above the median pro-social-score"
    pss_below = "Below the median pro-social-score"
    psscores = (pss_above,  pss_below)


class Subsession(BaseSubsession):

    def _get_stats(self, responses):
        means, stds = [], []
        for qanswers in zip(*responses.values()):
            means.append(stats.mean(qanswers))
        return tuple(means), tuple(stds)

    def _normalize(self, responses, means, stds):
        norms = {}
        for player, answers in responses.items():
            norms[player] = [
                (a-mean)/sigma for a, mean, sigma in zip(answers, means, stds)]
        return norms

    def set_ttype(self):
        responses = {}
        for player in self.get_players():
            responses[player] = [
                player.people_best_intentions,
                player.will_to_return_a_favor,
                player.give_to_without_expecting_anything_in_return,
                player.donate, player.present,
            ]
        means, stds = self._get_stats(responses)
        nomalized = self._normalize(responses, means, stds)




class Group(BaseGroup):
    pass


class Player(BasePlayer):

    ps_score = models.CharField(max_length=max(map(len, Constants.psscores)))

    computer = models.CharField(
        max_length=10,
        verbose_name="What computer are you sitting at?")
    gender = models.CharField(
        max_length=6, choices=["Male", "Female"],
        widget=widgets.RadioSelectHorizontal,
        verbose_name="What is your gender?")

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
        choices=list(sorted(Constants.presents.items())))

