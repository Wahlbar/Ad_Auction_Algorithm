# This class defines the advertiser.
import numpy as np

# //TODO: What are the essential differences between retailer and economic opportunity advertisers?
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

    def __init__(self):

        self.variance_utility_per_impression = 0.7
        self.sigma_utility_per_impression = np.sqrt(self.variance_utility_per_impression)

        ratio_advertisers = 0.9
        self.advertiser_type = np.random.choice(["r", "e"], 1, p=[ratio_advertisers,
                                                                  1 - ratio_advertisers])  # ratio retailer to economic opportunity

        # Draw ad quality from a random number between 0 and 1?
        # Right now I am generating the ad quality from a log normal distribution for only positive values.
        self.adQuality = np.random.lognormal(-5, 0.5, 1)  # normal distribution, power law distribution

        # Assign to all advertisers the same ad budget. Later change it depending on the type of advertiser.
        self.budget = 10000  # start with large budget for everyone //TODO: How to stretch the bid according to the budget?
        self.utility_per_impression = 0
        self.bid = 0
        self.list_of_users_won_per_slot = []
        self.mu_utility_per_impression_retailer_male = -3.5
        self.mu_utility_per_impression_retailer_female = -2.4
        self.mu_utility_per_impression_economic = -2.8

        if self.advertiser_type == "r":
            self.mu_utility_per_impression = 0
            Advertiser.nb_retailer += 1
        if self.advertiser_type == "e":
            self.mu_utility_per_impression = -2.8
            Advertiser.nb_economic_opportunity += 1

    def __str__(self):
        return "Advertiser: " \
               " advertiser type: %s" \
               " quality: %s" \
               " utility: %s" \
               " budget: %s" \
               " bid: %s" % (self.advertiser_type, self.adQuality, self.utility_per_impression, self.budget, self.bid)

    # utility = bid = click_through_rate * utility_per_click (vary utility depending on the user)
    # utility2 = utility_per_impression (vary depending on the user)
    # effective bid = pos * quality * bid (leave it away)

    # //TODO: Fix Revenue size!
    def bidding(self, user):
        if self.advertiser_type == "r" and user.sex == "m":
            self.mu_utility_per_impression = -3.5
        if self.advertiser_type == "r" and user.sex == "f":
            self.mu_utility_per_impression = -2.4
        self.utility_per_impression = np.random.lognormal(self.mu_utility_per_impression, self.sigma_utility_per_impression, 1)
        self.bid = user.click_through_rate * self.utility_per_impression

        # TODO: Make bidding more dynamic!
        # The advertiser cannot get below 0 budget.
        if self.budget - self.bid <= 0:
            self.bid = self.budget

        return self.bid

    def pay(self, bid):
        self.budget -= bid
        return

    def K_parity(self, user, probability_of_male_user):
        return
