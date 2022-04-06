# This class defines the advertiser.
import numpy as np

# TODO: What are the essential differences between retailer and economic opportunity advertisers?
''' 1. Retailer: 
    High Budget
    Allowed/Interested in discrimination --> targeting of protected groups
    High Ratio of retailers to economic advertisers
    2. Economic:
    (Lower Budget)
    Non-discriminatory behavior
    Depending on factors for economic opportunity.'''


class Advertiser:
    nb_retailer = 0
    nb_economic_opportunity = 0

    def __init__(self, list_parameters):

        # save the parameters
        self.parameters = list_parameters

        # save the variance for the utility per impression
        self.variance_utility_per_impression = float(self.parameters['variance_utility_per_impression'])
        self.sigma_utility_per_impression = np.sqrt(self.variance_utility_per_impression)

        # ratio of retailers to economic advertisers
        ratio_advertisers = float(self.parameters['ratio_advertisers'])
        self.advertiser_type = np.random.choice(["r", "e"], 1, p=[ratio_advertisers,
                                                                  1 - ratio_advertisers])

        # Draw ad quality from a random number between 0 and 1?
        # Right now I am generating the ad quality from a log normal distribution for only positive values.
        self.adQuality = np.random.lognormal(-5, 0.5, 1)  # normal distribution, power law distribution

        # Assign to all advertisers the same ad budget. Later change it depending on the type of advertiser.
        # TODO: @Stefania: How to stretch the bid according to the budget?
        self.budget = float(self.parameters['budget'])  # start with large budget for everyone //
        self.bid = 0
        self.utility_per_click_retailer_male = np.random.lognormal(float(self.parameters['mu_utility_per_impression_retailer_male']),
                                                                   self.sigma_utility_per_impression, 1)
        self.utility_per_click_retailer_female = np.random.lognormal(float(self.parameters['mu_utility_per_impression_retailer_female']),
                                                                     self.sigma_utility_per_impression, 1)
        self.utility_per_click_economic = np.random.lognormal(float(self.parameters['mu_utility_per_impression_economic']),
                                                              self.sigma_utility_per_impression, 1)
        self.utility_per_click = 0

    # utility = bid = click_through_rate * utility_per_click (vary utility depending on the user)
    # utility2 = utility_per_impression (vary depending on the user)
    # effective bid = pos * quality * bid (leave it away)

    # //TODO: Fix Revenue size!
    def gsp_bidding(self, user):
        if self.advertiser_type == "r" and user.sex == "m":
            self.utility_per_click = self.utility_per_click_retailer_male
        elif self.advertiser_type == "r" and user.sex == "f":
            self.utility_per_click = self.utility_per_click_retailer_female
        elif self.advertiser_type == "e":
            self.utility_per_click = self.utility_per_click_economic

        self.bid = self.utility_per_click * user.click_through_rate

        # TODO: Make bidding more dynamic! Only one person strategizes maybe? Only if strategies are directly related to genders! Only Economic advertisers strategize?!
        # The advertiser cannot get below 0 budget.
        if self.budget - self.bid <= 0:
            self.bid = self.budget

        return self.bid

    def pay(self, bid):
        self.budget -= bid
        return

    def k_parity_bidding(self, user, probability_of_male_user):
        return

    def k_ratio_bidding(self, user, probability_of_male_user):
        return

    def strategic_budget_bidding(self):
        return

