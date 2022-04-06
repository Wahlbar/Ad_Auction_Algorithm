# This class defines the user.
import numpy as np
import population
from scipy import stats


class User:

    def __init__(self, list_parameters):

        # save the parameters
        self.parameters = list_parameters

        # ratio of female to male users
        ratio_sex_users = float(self.parameters['ratio_sex_users'])
        mu_click_through_rate = float(self.parameters["mu_click_through_rate"])
        sigma_click_through_rate = float(self.parameters["sigma_click_through_rate"])

        self.sex = np.random.choice(["f", "m"], 1, p=[ratio_sex_users, 1 - ratio_sex_users])  # ratio of male to female

        self.age = np.random.choice(population.Population().age, 1, population.Population().age_distributions)

        # TODO: Refine attributes of users!
        # random number between 0 and 1, Not fixed attribute... -> constant, being dependent on user an ad.
        self.proximity = np.random.uniform(0, 1)

        # Closeness of the user's education level to the required job education.
        # If the user is too well educated the education similarity decreases again.
        # maybe generate a correlation in comparison to the age, not property of the agent! -> depends on user and ad.
        self.educationSimilarity = np.random.uniform(0, 1)

        # TODO: To test dependencies of the different attributes use correlation between
        # TODO: @Stefania: Is this a good way to estimate the users' click through rates?
        # Average click through rate on Google 3.17% -> Does the click through rate differ in the bidding algorithm based on sex or only on position?
        self.click_through_rate = stats.truncnorm.rvs(0, 1, loc=mu_click_through_rate, scale=sigma_click_through_rate, size=1)  # TODO: Read into click through rate! Different for every user but static? Or different for every position and static?
        # if self.sex == "f":
        #     # From Nasr and Tschanz: female = 1.71%
        #     self.click_through_rate = stats.truncnorm.rvs(0, 1, loc=0.0171, scale=0.005, size=1)
        # if self.sex == "m":
        #     # From Nasr and Tschanz: male = 0.97%
        #     self.click_through_rate = stats.truncnorm.rvs(0, 1, loc=0.0097, scale=0.005, size=1)
