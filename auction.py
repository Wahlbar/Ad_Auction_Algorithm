import user
import advertiser
import numpy as np


class Auction:

    # Define all import properties for a single auction.
    def __init__(self, list_parameters):
        self.parameters = list_parameters
        self.users = []
        self.advertisers = []
        self.slots_per_user = int(self.parameters['slots_per_user'])
        self.advertiser_size = int(self.parameters['advertiser_size'])
        self.ratio_user_advertiser = int(self.parameters['ratio_user_advertiser'])
        self.user_size = self.ratio_user_advertiser * self.advertiser_size

        # number of retailer and economic opportunity advertisers at each iteration
        self.no_retail_ads_total = 0
        self.no_economic_ads_total = 0

        self.no_retailer = 0
        self.no_economic = 0

        # number of female and male users at each iteration
        self.no_female = 0
        self.no_male = 0

        # number of retail ads shown to female and male users at each iteration
        self.no_retail_ads_female = 0
        self.no_retail_ads_male = 0

        # number of economic opportunity ads shown to female and male users at each iteration
        self.no_economic_ads_female = 0
        self.no_economic_ads_male = 0

        # sum of positions in retail and economic ads
        self.sum_position_retail_male = 0
        self.sum_position_economic_male = 0
        self.sum_position_retail_female = 0
        self.sum_position_economic_female = 0

        # average position of retail and economic ads
        self.avg_position_retail_male = 0
        self.avg_position_economic_male = 0
        self.avg_position_retail_female = 0
        self.avg_position_economic_female = 0

        # platform revenue
        self.platform_revenue = 0

    # Generate the users for the auction.
    def generate_users(self, no_users):
        for i in range(no_users):
            self.users.append(user.User(self.parameters))

    # Generate the advertisers for the action.
    def generate_advertisers(self, no_advertisers):
        for i in range(no_advertisers):
            self.advertisers.append(advertiser.Advertiser(self.parameters))

    def auctioning(self):
        """
        Performs one iteration of the auction.
        0. A new user arrives.
        1. Advertiser bid on the user according to their budget, impression and the users click through rate.
        2. The platform takes the top 10 bidders as the winner.
        3. The bidder pay according to the next position.
        4. The data is collected: amount of retailer per male/female & economic per male/female.
        """

        # Count the advertisers:
        self.count_advertisers()

        # 0.
        for current_user in self.users:

            # 1.
            for current_advertiser in self.advertisers:
                current_advertiser.gsp_bidding(current_user)
                # If the advertiser is sold out, remove him from the bid
                if current_advertiser.bid == 0:
                    self.advertisers.remove(current_advertiser)
            # Breaking ties is not very important since the probability of getting two similar numbers is very low due to the continuous space.
            # Here the ties are not broken randomly.
            # 2.
            # Check if there are no advertisers able to bid anymore and break if so.
            if not self.advertisers:
                break
            sorted_advertiser_by_bid = sorted(self.advertisers, key=lambda adv: adv.bid, reverse=True)
            winning_advertisers = sorted_advertiser_by_bid[:self.slots_per_user]

            # 3. For each winner get the position of the next advertiser and pay its bid to the platform.
            second_price_index = 1
            for current_advertiser in winning_advertisers:

                if second_price_index < len(sorted_advertiser_by_bid):
                    next_advertiser = sorted_advertiser_by_bid[second_price_index] # TODO: @Stefania: What does the last advertiser pay?
                    cost = next_advertiser.bid
                else:
                    cost = np.random.uniform(0, current_advertiser.bid)
                self.platform_revenue += cost
                current_advertiser.pay(next_advertiser.bid)
                second_price_index += 1

            # 4.
            self.save_statistics(current_user, winning_advertisers)

        self.calculate_avg_positions()

    # Function to save the important statistics.
    def save_statistics(self, current_user, winning_advertisers):

        if current_user.sex == "m":
            self.no_male += 1
            for current_advertiser in winning_advertisers:
                if current_advertiser.advertiser_type == "r":
                    self.no_retail_ads_male += 1
                    self.no_retail_ads_total += 1
                    self.sum_position_retail_male += winning_advertisers.index(current_advertiser)
                elif current_advertiser.advertiser_type == "e":
                    self.no_economic_ads_male += 1
                    self.no_economic_ads_total += 1
                    self.sum_position_economic_male += winning_advertisers.index(current_advertiser)
        elif current_user.sex == "f":
            self.no_female += 1
            for current_advertiser in winning_advertisers:
                if current_advertiser.advertiser_type == "r":
                    self.no_retail_ads_female += 1
                    self.no_retail_ads_total += 1
                    self.sum_position_retail_female += winning_advertisers.index(current_advertiser)
                elif current_advertiser.advertiser_type == "e":
                    self.no_economic_ads_female += 1
                    self.no_economic_ads_total += 1
                    self.sum_position_economic_female += winning_advertisers.index(current_advertiser)

    def calculate_avg_positions(self):
        if self.no_retail_ads_male == 0:
            self.avg_position_retail_male = 0
        else:
            self.avg_position_retail_male = self.sum_position_retail_male/self.no_retail_ads_male

        if self.no_economic_ads_male == 0:
            self.avg_position_economic_male = 0
        else:
            self.avg_position_economic_male = self.sum_position_economic_male/self.no_economic_ads_male

        if self.no_retail_ads_female == 0:
            self.avg_position_retail_female = 0
        else:
            self.avg_position_retail_female = self.sum_position_retail_female/self.no_retail_ads_female

        if self.no_economic_ads_female == 0:
            self.avg_position_economic_female = 0
        else:
            self.avg_position_economic_female = self.sum_position_economic_female/self.no_economic_ads_female

    def count_advertisers(self):
        for current_advertiser in self.advertisers:
            if current_advertiser.advertiser_type == "r":
                self.no_retailer += 1
            elif current_advertiser.advertiser_type == "e":
                self.no_economic += 1
        return
