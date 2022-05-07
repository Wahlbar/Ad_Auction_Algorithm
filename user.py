# This class defines the user.
import numpy as np
import population
from scipy import stats

''' 
This class defines the user and its parameters
There are currently two (binary) types of users:
female users: valued higher by retail advertisers --> competition overflow
--> more expensive for economic opportunity advertisers --> reached less 
--> discrimination/unfair.
male users: valued lower by retail advertisers.
'''


class User:

    """
    Define the most important variables for the user.
    """
    def __init__(self, list_parameters):

        # Save the configuration parameters given by the config file.
        self.parameters = list_parameters

        # Save the ratio of female to male users.
        # For each user the type is randomly generated with the probabilities given by the ratio of female to male users.
        ratio_sex_users = float(self.parameters['ratio_sex_users'])
        self.sex = np.random.choice(["f", "m"], 1, p=[ratio_sex_users, 1 - ratio_sex_users])  # ratio of male to female

        # Save the true click through rate mean and standard deviation to generate the users true click through rate.
        # Unused right now.
        mu_click_through_rate = float(self.parameters["mu_click_through_rate"])
        sigma_click_through_rate = float(self.parameters["sigma_click_through_rate"])

        # Generate the user's age based on the distribution of the swiss population. Unused right now...
        self.age = np.random.choice(population.Population().age, 1, population.Population().age_distributions)

        # TODO: Refine attributes of users!
        # random number between 0 and 1, Not fixed attribute... -> constant, being dependent on user an ad.
        # Generate a proximity factor of the user. (Proximity to job location.) Not sure if this is a useful attribute.
        # Unused right now.
        self.proximity = np.random.uniform(0, 1)

        # Closeness of the user's education level to the required job education.
        # If the user is too well educated the education similarity decreases again.
        # Maybe generate a correlation in comparison to the age, not property of the agent! -> depends on user and ad.
        # The education similarity should be considered between the advertiser and the user.
        # Adjust it correctly.
        # TODO: change
        # Unused right now.
        self.educationSimilarity = np.random.uniform(0, 1)

        # TODO: To test dependencies of the different attributes use correlation between
        # These variables would be to calculate the true click through rate of the users.
        # Drawn from a distribution between 0 and 1 and based on the given mean and standard deviation. --> From empirical values.
        # Unused right now.
        # Average click through rate on Google 3.17% -> Does the click through rate differ in the bidding algorithm based on sex or only on position?
        self.true_click_probability = stats.truncnorm.rvs(0, 1, loc=mu_click_through_rate, scale=sigma_click_through_rate, size=1)
        # if self.sex == "f":
        #     # From Nasr and Tschanz: female = 1.71%
        #     self.click_through_rate = stats.truncnorm.rvs(0, 1, loc=0.0171, scale=0.005, size=1)
        # if self.sex == "m":
        #     # From Nasr and Tschanz: male = 0.97%
        #     self.click_through_rate = stats.truncnorm.rvs(0, 1, loc=0.0097, scale=0.005, size=1)
