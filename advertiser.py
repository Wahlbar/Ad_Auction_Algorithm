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
        self.variance_estimated_value_per_click = float(self.parameters['variance_estimated_value_per_click'])
        self.sigma_estimated_value_per_click = np.sqrt(self.variance_estimated_value_per_click)

        # ratio of retailers to economic advertisers
        ratio_advertisers = float(self.parameters['ratio_advertisers'])
        self.advertiser_type = np.random.choice(["r", "e"], 1, p=[ratio_advertisers,
                                                                  1 - ratio_advertisers])

        # Assign to all advertisers the same ad budget. Later change it depending on the type of advertiser.
        # TODO: @Stefania: How to stretch the bid according to the budget?
        self.budget = float(self.parameters['budget'])  # start with large budget for everyone //
        self.estimated_value = 0
        self.bid = 0
        self.mu_estimated_value_per_click_retailer_male = float(self.parameters['mu_estimated_value_per_click_retailer_male'])
        self.mu_estimated_value_per_click_retailer_female = np.random.lognormal(float(self.parameters['mu_estimated_value_per_click_retailer_female']),
                                                                                self.sigma_estimated_value_per_click, 1)
        self.mu_estimated_value_per_click_economic = np.random.lognormal(float(self.parameters['mu_estimated_value_per_click_economic']),
                                                                         self.sigma_estimated_value_per_click, 1)
        self.estimated_value_per_click = 0
        self.estimated_quality = 1

    # utility = bid = click_through_rate * utility_per_click (vary utility depending on the user)
    # utility2 = utility_per_impression (vary depending on the user)
    # effective bid = pos * quality * bid (leave it away)

    # click through rate = quality * position

    # //TODO: Fix Revenue size!
    def gsp_truthful_bidding(self, user):
        if self.advertiser_type == "r" and user.sex == "m":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_retailer_male,
                                                                 self.sigma_estimated_value_per_click, 1)
        elif self.advertiser_type == "r" and user.sex == "f":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_retailer_female,
                                                                 self.sigma_estimated_value_per_click, 1)
        elif self.advertiser_type == "e":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_economic,
                                                                 self.sigma_estimated_value_per_click, 1)

        self.estimated_value = self.estimated_value_per_click * self.estimated_quality

        # TODO: Make bidding more dynamic! Only one person strategizes maybe? Only if strategies are directly related to genders! Only Economic advertisers strategize?!
        # The advertiser cannot get below 0 budget.
        if (self.budget - self.estimated_value) <= 0:
            self.estimated_value = self.budget

        self.bid = self.estimated_value
        return self.estimated_value

    def pay(self, cost):
        if cost >= self.budget:
            self.budget = 0
        else:
            self.budget -= cost
        return

    def k_parity_bidding(self, user, probability_of_male_user):
        return

    def k_ratio_bidding(self, user, probability_of_male_user):
        return

    def strategic_budget_bidding(self):
        return

    def set_bid(self, bid):
        self.bid = bid
        return

