import copy
import user
import advertiser


class Auction:

    def __init__(self, list_parameters, users=[], advertisers=[],
                 no_retailer=0, no_economic=0,
                 no_female=0, no_male=0, no_retail_ads_female=0, no_retail_ads_male=0,
                 no_economic_ads_female=0, no_economic_ads_male=0, platform_revenue=0):
        self.parameters = list_parameters
        self.users = copy.deepcopy(users)
        self.advertisers = copy.deepcopy(advertisers)
        self.slots_per_user = int(self.parameters['slots_per_user'])
        self.advertiser_size = int(self.parameters['advertiser_size'])
        self.user_size = int(self.parameters['user_size'])

        # number of retailer and economic opportunity advertisers at each iteration
        self.no_retailer = no_retailer
        self.no_economic = no_economic

        # number of female and male users at each iteration
        self.no_female = no_female
        self.no_male = no_male

        # number of retail ads shown to female and male users at each iteration
        self.no_retail_ads_female = no_retail_ads_female
        self.no_retail_ads_male = no_retail_ads_male

        # number of economic opportunity ads shown to female and male users at each iteration
        self.no_economic_ads_female = no_economic_ads_female
        self.no_economic_ads_male = no_economic_ads_male

        # platform revenue
        self.platform_revenue = platform_revenue

    def write(self):
        """Writes the amount of retailer/economic ads shown to female/male users and the platform revenue."""
        print("Number of economic ads for male users: ", self.no_economic_ads_male)
        print("Number of economic ads for female users: ", self.no_economic_ads_female)
        print("Number of retail ads for male users: ", self.no_retail_ads_male)
        print("Number of retail ads for male users: ", self.no_retail_ads_female)
        print("Revenue: ", self.platform_revenue)

    def generate_users(self, no_users):
        for i in range(no_users):
            self.users.append(user.User())

    def generate_advertisers(self, no_advertisers):
        for i in range(no_advertisers):
            self.advertisers.append(advertiser.Advertiser())

    # utility = bid = click_through_rate * utility_per_click (utility per click is independent from sex -> constant.)
    # effective bid = pos * quality * bid (leave it away)

    def bidding(self):
        """
        Performs one iteration of the auction.
        0. A new user arrives.
        1. Advertiser bid on the user according to their budget, impression and the users click through rate.
        2. The platform takes the top 10 bidders as the winner. TODO: Break ties randomly?
        3. The bidder pay according to the next position.
        4. The data is collected: amount of retailer per male/female & economic per male/female.
        """

        for user in self.users:
            for advertiser in self.advertisers:
                advertiser.bidding(user)
            # TODO: break ties! How to do it? -> Argue: not probable to happen? Is this enough?
            # TODO: Maybe use order: score to break ties!
            sorted_advertiser_by_bid = sorted(self.advertisers, key=lambda advertiser: advertiser.bid, reverse=True)
            # sorted_advertiser_by_bid = heapq.nlargest(self.slots_per_user, self.advertisers, key=lambda advertiser: advertiser.bid, reverse=True)
            winning_advertisers = sorted_advertiser_by_bid[:self.slots_per_user]

            # For each winner get the position of the next advertiser and pay its bid to the platform.
            for advertiser in winning_advertisers:
                second_price_index = 1
                next_advertiser = sorted_advertiser_by_bid[second_price_index]
                self.platform_revenue += next_advertiser.bid
                advertiser.pay(next_advertiser.bid)
                second_price_index += 1

            self.save_statistics(user, winning_advertisers)

    def save_statistics(self, user, winning_advertisers):

        if user.sex == "m":
            self.no_male += 1
            for advertiser in winning_advertisers:
                if advertiser.advertiser_type == "r":
                    self.no_retail_ads_male += 1
                    self.no_retailer += 1
                elif advertiser.advertiser_type == "e":
                    self.no_retail_ads_male += 1
                    self.no_economic += 1
        elif user.sex == "f":
            self.no_female += 1
            for advertiser in winning_advertisers:
                if advertiser.advertiser_type == "r":
                    self.no_retail_ads_female += 1
                    self.no_retailer += 1
                elif advertiser.advertiser_type == "e":
                    self.no_economic_ads_female += 1
                    self.no_economic += 1
