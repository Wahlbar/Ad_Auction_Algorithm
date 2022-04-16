import user
import advertiser
import numpy as np


class Auction:

    # Define all import properties for a single auction.
    def __init__(self, list_parameters):
        self.parameters = list_parameters
        self.users = []
        self.advertisers = []
        self.sorted_advertiser_by_estimated_value = []

        self.slots_per_user = int(self.parameters['slots_per_user'])
        self.advertiser_size = int(self.parameters['advertiser_size'])
        self.ratio_user_advertiser = int(self.parameters['ratio_user_advertiser'])
        self.user_size = self.ratio_user_advertiser * self.advertiser_size

        self.position_effects = []
        self.calculate_position_effects()

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

        # truthful platform revenue
        self.truthful_platform_revenue = 0

        # reserve price TODO: Argue why!
        self.reserve_price = 0.5

    # Generate the users for the auction.
    def generate_users(self, no_users):
        for i in range(no_users):
            self.users.append(user.User(self.parameters))
        return self.users

    def set_users(self, users):
        self.users = users

    # Generate the advertisers for the action.
    def generate_advertisers(self, no_advertisers):
        for i in range(no_advertisers):
            self.advertisers.append(advertiser.Advertiser(self.parameters))
        return self.advertisers

    def set_advertisers(self, advertisers):
        self.advertisers = advertisers

    def calculate_position_effects(self):
        for i in range(self.slots_per_user):
            self.position_effects.append((self.slots_per_user - i)/self.slots_per_user)

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
                current_advertiser.gsp_truthful_bidding(current_user)
                # If the advertiser is sold out, remove him from the bid
                if current_advertiser.estimated_value == 0:
                    self.advertisers.remove(current_advertiser)
            # Breaking ties is not very important since the probability of getting two similar numbers is very low due to the continuous space.
            # Here the ties are not broken randomly.
            # 2.
            # Check if there are no advertisers able to bid anymore and break if so.
            if not self.advertisers:
                break
            self.sorted_advertiser_by_estimated_value = sorted(self.advertisers, key=lambda adv: adv.estimated_value, reverse=True)
            winning_advertisers = self.sorted_advertiser_by_estimated_value[:self.slots_per_user]

            # remove advertiser with a too low estimated_value from the winning list
            for current_advertiser in winning_advertisers:
                # remove advertiser with a too low estimated_value
                if current_advertiser.estimated_value < self.reserve_price:
                    winning_advertisers.remove(current_advertiser)

            # Calculate the envy free bids
            envy_free_bids = self.calculate_utilities(winning_advertisers, self.reserve_price)

            # 3. For each winner get the position of the next advertiser and pay its bid to the platform.
            # Run it once with truthful bidding and once with the strategized bidding. 
            second_price_index = 1
            for bid in envy_free_bids:
                if second_price_index < len(envy_free_bids):
                    next_bid = envy_free_bids[second_price_index]
                    cost = next_bid
                else:
                    cost = self.reserve_price
                self.platform_revenue += cost
                winning_advertisers[envy_free_bids.index(bid)].pay(cost)
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

# WORKS!
    def calculate_utilities(self, winning_advertisers, min_price):
        maximized_utilities = []
        for current_advertiser in reversed(winning_advertisers):
            position_index = winning_advertisers.index(current_advertiser)
            if position_index == len(winning_advertisers) - 1:
                next_lower_bid = min_price
            else:
                next_advertiser = winning_advertisers[position_index+1]
                next_lower_bid = next_advertiser.bid
            if position_index == 0:
                best_bid = current_advertiser.estimated_value
            else:
                best_bid = current_advertiser.estimated_value - (self.position_effects[position_index]/self.position_effects[position_index-1] * (current_advertiser.estimated_value - next_lower_bid))
            current_advertiser.set_bid(best_bid)
            maximized_utilities.append(best_bid)
        maximized_utilities.sort(reverse=True)
        return maximized_utilities

    def calculate_avg_positions(self):
        if self.no_retail_ads_male == 0:
            self.avg_position_retail_male = 0
        else:
            self.avg_position_retail_male = self.sum_position_retail_male / self.no_retail_ads_male

        if self.no_economic_ads_male == 0:
            self.avg_position_economic_male = 0
        else:
            self.avg_position_economic_male = self.sum_position_economic_male / self.no_economic_ads_male

        if self.no_retail_ads_female == 0:
            self.avg_position_retail_female = 0
        else:
            self.avg_position_retail_female = self.sum_position_retail_female / self.no_retail_ads_female

        if self.no_economic_ads_female == 0:
            self.avg_position_economic_female = 0
        else:
            self.avg_position_economic_female = self.sum_position_economic_female / self.no_economic_ads_female

    def count_advertisers(self):
        for current_advertiser in self.advertisers:
            if current_advertiser.advertiser_type == "r":
                self.no_retailer += 1
            elif current_advertiser.advertiser_type == "e":
                self.no_economic += 1
        return
