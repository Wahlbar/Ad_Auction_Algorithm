# This class defines the user.
import numpy as np
import population
from scipy import stats

class User:
    nb_male = 0
    nb_female = 0

    def __init__(self):
        ratio_sex_users = 0.5
        self.sex = np.random.choice(["f", "m"], 1, p=[ratio_sex_users, 1 - ratio_sex_users]) # ratio of male to female
        self.age = np.random.choice(population.Population().age, 1, population.Population().age_distributions)
        self.proximity = np.random.uniform(0, 1) # random number between 0 and 1, Not fixed attribute... -> constant, being dependent on user an ad.
        # Closeness of the user's education level to the required job education.
        # If the user is too well educated the education similarity decreases again.
        self.educationSimilarity = np.random.uniform(0, 1) # maybe generate a correlation in comparison to the age, not property of the agent! -> depends on user and ad.
        # To test dependencies of the different attributes use correlation between
        # //TODO: Different Click Rates for females and males? Yes, no?
        # Average click through rate on Google 3.17%
        self.click_through_rate = stats.truncnorm.rvs(0, 1, loc = 0.0317, scale = 0.01, size = 1)
        if self.sex == "f":
            User.nb_female += 1
            self.click_through_rate = stats.truncnorm.rvs(0, 1, loc = 0.0171, scale = 0.005, size = 1) # From Nasr and Tschanz: female = 1.71%
        if self.sex == "m":
            User.nb_male += 1
            self.click_through_rate = stats.truncnorm.rvs(0, 1, loc = 0.0097, scale = 0.005, size = 1) # From Nasr and Tschanz: male = 0.97%

    def __str__(self):
        return "User: " \
               " sex: %s" \
               " age: %s" \
               " proximity: %s" \
               " education similarity: %s" \
               " click through rate: %s" % (self.sex, self.age, self.proximity, self.educationSimilarity, self.click_through_rate)

