# TODO: Maybe put into csv later on!
# TODO: Adjust the populations corresponding to social media users.
# This class is unused right now.
# It takes the age distribution of the swiss population to assign a users' age with the same probability as in the swiss population.
# However the user's age is not taken into consideration during estimating the expected value per click.
# --> Not useful.
class Population:
    def __init__(self):
        self.age = list(range(18, 66))
        self.age_distributions = [0.016773035, 0.016987166, 0.018104506, 0.018027632, 0.018285909, 0.018604569,
                                  0.019118332, 0.018932362, 0.019150045, 0.019393354, 0.020142052, 0.020230343,
                                  0.020219941, 0.019852062, 0.019859419, 0.01912848, 0.019285527, 0.018968389,
                                  0.019072664, 0.018884411, 0.019258887, 0.019195713, 0.019333224, 0.019006446,
                                  0.018793583, 0.018955957, 0.019013042, 0.019249246, 0.020065178, 0.020596955,
                                  0.021475046, 0.022609638, 0.023130758, 0.02404995, 0.024723044, 0.02516932,
                                  0.025830489, 0.026106272, 0.026513476, 0.026023308, 0.02505921, 0.024355925,
                                  0.023589974, 0.023093209, 0.022312543, 0.021945171, 0.021192666, 0.020331574]
