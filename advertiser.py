import numpy as np

''' 
This class defines the advertiser, its parameters and allows the advertisers to bid.
There are currently two (binary) types of advertisers:
retail advertiser: prefer female users over male users --> estimate a higher value per click for female users
economic opportunity advertisers: don't distinguish between female and male users --> estimate same value per click for both genders.
The estimated value per clicks are drawn from log-normal distributions.
'''


class Advertiser:

    """
    Define the most important variables for the advertiser.
    """
    def __init__(self, list_parameters):

        # Save the configuration parameters given by the config file.
        self.parameters = list_parameters

        # Save the variance and standard deviation for the value per click.
        self.variance_estimated_value_per_click = float(self.parameters['variance_estimated_value_per_click'])
        self.sigma_estimated_value_per_click = np.sqrt(self.variance_estimated_value_per_click)

        # Save the ratio of retail to economic opportunity advertisers.
        # For each advertiser the type is randomly generated with the probabilities given by the ratio of retail to economic opportunity advertisers.
        ratio_advertisers = float(self.parameters['ratio_advertisers'])
        self.advertiser_type = np.random.choice(["r", "e"], 1, p=[ratio_advertisers,
                                                                  1 - ratio_advertisers])

        # Save the budget of the advertisers.
        # TODO: Maybe make more dynamic budgets.
        self.budget = float(self.parameters['budget'])

        # Define the estimated value.
        self.estimated_value = 0

        # Define the bid.
        self.bid = 0

        # TODO: Save the mu in dependence of the advertiser type!
        # Save the mu for the lognormal distribution for the estimated value per click for retail advertisers (male and female).
        self.mu_estimated_value_per_click_retailer_male = float(self.parameters['mu_estimated_value_per_click_retailer_male'])
        self.mu_estimated_value_per_click_retailer_female = np.random.lognormal(float(self.parameters['mu_estimated_value_per_click_retailer_female']),
                                                                                self.sigma_estimated_value_per_click, 1)
        # Save the mu for the lognormal distribution for the estimated value per click for economic opportunity advertisers.
        self.mu_estimated_value_per_click_economic = np.random.lognormal(float(self.parameters['mu_estimated_value_per_click_economic']),
                                                                         self.sigma_estimated_value_per_click, 1)
        # Define the estimated value per click.
        self.estimated_value_per_click = 0

        # Define the estimated quality
        # TODO: Make the estimated quality dynamic (depending on correlation to user interests).
        self.estimated_quality = 1

    '''
    In this method the advertiser estimates the users value per click based on their parameters.
    (Here only gender.)
    These estimations are drawn for lognormal distributions.
    '''
    def gsp_truthful_bidding(self, user):
        # TODO: Make the bidding only from the advertisers type depending --> one if check less!
        # Check the type of the advertiser and the user type and depending on them draw the estimated value per click from different distributions.
        if self.advertiser_type == "r" and user.sex == "m":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_retailer_male,
                                                                 self.sigma_estimated_value_per_click, 1)
        elif self.advertiser_type == "r" and user.sex == "f":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_retailer_female,
                                                                 self.sigma_estimated_value_per_click, 1)
        elif self.advertiser_type == "e":
            self.estimated_value_per_click = np.random.lognormal(self.mu_estimated_value_per_click_economic,
                                                                 self.sigma_estimated_value_per_click, 1)

        # Value = Value per click * Quality
        self.estimated_value = self.estimated_value_per_click * self.estimated_quality

        # TODO: Let the advertiser strategise more. (If all advertiser have low budget, act differently?)
        # The advertiser cannot get below 0 budget.
        if (self.budget - self.estimated_value) <= 0:
            self.estimated_value = self.budget

        # Assign the bid as the estimated value (truthful).
        self.bid = self.estimated_value
        return self.estimated_value

    '''
    This method let the advertiser pay. 
    '''
    def pay(self, cost):
        # If the cost is higher than the budget, set the budget to 0 --> no negative budget possible
        if cost >= self.budget:
            self.budget = 0
        else:
            self.budget -= cost
        return

    '''
    This method sets the bid.
    '''
    def set_bid(self, bid):
        self.bid = bid
        return

    '''
    This method resets the advertisers budget --> for multiple concurrent auctions.
    '''
    def reset_budget(self):
        self.budget = float(self.parameters['budget'])