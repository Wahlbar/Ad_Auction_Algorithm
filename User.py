# This class defines the user.
import numpy as np


class User:
    def __init__(self, sex, age, prox, edu):
        sigma = np.sqrt(0.7)
        mu_economic_opportunity = -2.8
        mu_retailer = 0

        self.sex = sex
        self.age = age
        self.proximity = prox
        self.education = edu

        if self.sex == "f":
            mu_retailer = -2.4
        elif self.sex == "m":
            mu_retailer = -3.5
        self.retailValue = np.random.lognormal(mu_retailer, sigma, 1)
        self.economicOpportunityValue = np.random.lognormal(mu_economic_opportunity, sigma, 1)

    def __str__(self):
        return "User: " \
               " sex: %s" \
               " age: %s" \
               " proximity: %s" \
               " education: %s" \
               " retail value: %s" \
               " economic opportunity value: %s" % (self.sex, self.age, self.proximity, self.education, self.retailValue, self.economicOpportunityValue)

    def generateClickThroughRate(self, quality):
        # If the user attributes are close to the quality -> high click-through rate?
        return
