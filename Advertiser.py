# This class defines the advertiser.

class Advertiser:
    def __init__(self, advertiser_type, quality, utility, budget):
        self.advertiserType = advertiser_type
        self.adQuality = quality  # normal distribution, power law distribution
        self.utility_per_click = utility  # draw from normal distribution -> what kind of? -> depends on retailing
        # product.
        self.budget = budget  # start with large budget for everyone

    def __str__(self):
        return "Advertiser: " \
               " advertiser type: %s" \
               " quality: %s" \
               " utility: %s" \
               " budget: %s" % (self.advertiserType, self.adQuality, self.utility_per_click, self.budget)

    # utility = bid = click_through_rate * utility_per_click (utility per click is independent from sex -> constant.)
    # effective bid = pos * quality * bid (leave it away)

    def estimateUserValue(User):
        return
