import user
import advertiser

'''
This class defines the unrestrained gsp auction. 
It contains a lot of variables to track the output parameters.
It generates the users and advertisers.
Additionally it also contains all methods to auction the users to the advertisers.
'''

# TODO: Extract an interface/superclass from this
#  and implement two similar auctions --> less redundant code.

class Unrestrained_Auction:

    # Define all import properties for a single auction.
    def __init__(self, list_parameters):
        # Save the configuration parameters given by the config file.
        self.parameters = list_parameters

        # Save the list of users and advertisers.
        self.users = []
        self.advertisers = []

        # Save the advertiser sorted by their estimated value (Redundant).
        # TODO: Remove!
        self.sorted_advertiser_by_estimated_value = []

        # Save the amount of slots per user, the advertiser size and the ratio of users to advertisers.
        self.slots_per_user = int(self.parameters['slots_per_user'])
        self.advertiser_size = int(self.parameters['advertiser_size'])
        self.ratio_user_advertiser = int(self.parameters['ratio_user_advertiser'])
        # Save the user size.
        self.user_size = self.ratio_user_advertiser * self.advertiser_size

        # Save the position effects for each slot (first to last).
        self.position_effects = []
        # Calculate the position effects and save them into the position effects.
        self.calculate_position_effects()

        # Number of retailer and economic opportunity advertisers who won the auction at each iteration.
        self.no_retail_ads_total = 0
        self.no_economic_ads_total = 0

        # Total number of retailers and economic opportunity advertisers generated.
        self.no_retailer = 0
        self.no_economic = 0

        # Total number of female and male users generated.
        self.no_female = 0
        self.no_male = 0

        # Number of retail ads shown to female and male users at each iteration.
        self.no_retail_ads_female = 0
        self.no_retail_ads_male = 0

        # Number of economic opportunity ads shown to female and male users at each iteration.
        self.no_economic_ads_female = 0
        self.no_economic_ads_male = 0

        # Sum of the positions of retail and economic ads for female and male users.
        # --> calculate average slot position later.
        self.sum_position_retail_male = 0
        self.sum_position_economic_male = 0
        self.sum_position_retail_female = 0
        self.sum_position_economic_female = 0

        # Average position of retail and economic ads for female and male users.
        self.avg_position_retail_male = 0
        self.avg_position_economic_male = 0
        self.avg_position_retail_female = 0
        self.avg_position_economic_female = 0

        # Platform revenue.
        self.platform_revenue = 0

        # Reserve price
        # TODO: Adjust reserve price according to the slot position!
        # TODO: Vary reserve prices. (reserve_price * position effect = end price = 0.5)
        self.reserve_price = 0.5

    # Generate the users for the auction.
    def generate_users(self, no_users):
        for i in range(no_users):
            self.users.append(user.User(self.parameters))
        return self.users

    # Set the users for the auction -> use the same set of users for different auction types.
    def set_users(self, users):
        self.users = users

    # Generate the advertisers for the action.
    def generate_advertisers(self, no_advertisers):
        for i in range(no_advertisers):
            self.advertisers.append(advertiser.Advertiser(self.parameters))
        return self.advertisers

    # Set the advertisers for the auction -> use the same set of advertisers for different auction types.
    def set_advertisers(self, advertisers):
        self.advertisers = advertisers

    # Calculates and saves the position effects in dependence of the slots per users.
    # The distance between the position effects is evenly distributed here.
    # TODO: Optional: Make the distances between the position effects not even.
    def calculate_position_effects(self):
        for i in range(self.slots_per_user):
            self.position_effects.append((self.slots_per_user - i)/self.slots_per_user)

    # This method performs the auction.
    # TODO: Split this method similar to the separated slots auction.
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

        # Iterate through the users.
        for current_user in self.users:

            # Iterate through the advertisers and let them estimate their expected value on the user.
            for current_advertiser in self.advertisers:
                current_advertiser.gsp_truthful_bidding(current_user)
                # If the advertiser is sold out, remove him from the list. --> Faster termination of the loop.
                if current_advertiser.estimated_value < self.reserve_price and current_advertiser.budget < self.reserve_price:
                    self.advertisers.remove(current_advertiser)

            # Breaking ties is not very important since the probability of getting two similar numbers is very low due to the continuous space.
            # Here the ties are not broken randomly.
            # Check if the advertiser list still contains advertisers.
            if not self.advertisers:
                break

            # Sort the list of advertisers by their estimated values and select the top x advertisers as winners, where x = number of slots available.
            self.sorted_advertiser_by_estimated_value = sorted(self.advertisers, key=lambda adv: adv.estimated_value, reverse=True)
            winning_advertisers = self.sorted_advertiser_by_estimated_value[:self.slots_per_user]

            # Remove advertiser with an estimated_value lower than the reserve price from the winning list.
            for current_advertiser in list(winning_advertisers):
                if current_advertiser.estimated_value < self.reserve_price:
                    winning_advertisers.remove(current_advertiser)

            # Calculate the optimized bids with the balanced bidding.
            optimized_bids = self.calculate_utilities(winning_advertisers, self.reserve_price)

            # For each winner get the position of the next advertiser and pay its bid to the platform.
            second_price_index = 1
            for bid in optimized_bids:
                # Check if the advertiser is not the last in the list.
                # If so, they pay the price of the next advertiser.
                if second_price_index < len(optimized_bids):
                    next_bid = optimized_bids[second_price_index]
                    cost = next_bid
                # Otherwise they pay the reserve price.
                else:
                    cost = self.reserve_price
                # Add the paid value to the platform revenue.
                self.platform_revenue += cost
                # Let the advertiser pay (reduce their budget).
                winning_advertisers[optimized_bids.index(bid)].pay(cost)
                second_price_index += 1

            # Save the statistics of the current user and their winning advertisers.
            self.save_statistics(current_user, winning_advertisers)

        # Calculate the average slot position of the different advertiser types.
        self.calculate_avg_positions()

    # Function to save the important statistics, for the output.
    def save_statistics(self, current_user, winning_advertisers):

        # Check if the current user is male.
        if current_user.sex == "m":
            # Increase the count of male users.
            self.no_male += 1
            # Iterate through the advertiser which won the auction, check their type and increase the corresponding count of ads shown to male users
            # and the count of total number of the corresponding ad type shown.
            # Save the position of the advertiser to the position sum, to later calculate the average slot position.
            for current_advertiser in winning_advertisers:
                # For retailers.
                if current_advertiser.advertiser_type == "r":
                    self.no_retail_ads_male += 1
                    self.no_retail_ads_total += 1
                    self.sum_position_retail_male += winning_advertisers.index(current_advertiser)
                # For economic opportunity advertisers.
                elif current_advertiser.advertiser_type == "e":
                    self.no_economic_ads_male += 1
                    self.no_economic_ads_total += 1
                    self.sum_position_economic_male += winning_advertisers.index(current_advertiser)
        # Same procedure for female users.
        elif current_user.sex == "f":
            # Increase the count of female users.
            self.no_female += 1
            # Iterate through the advertiser which won the auction, check their type and increase the corresponding count of ads shown to female users
            # and the count of total number of the corresponding ad type shown.
            # Save the position of the advertiser to the position sum, to later calculate the average slot position.
            for current_advertiser in winning_advertisers:
                # For retailers.
                if current_advertiser.advertiser_type == "r":
                    self.no_retail_ads_female += 1
                    self.no_retail_ads_total += 1
                    self.sum_position_retail_female += winning_advertisers.index(current_advertiser)
                # For economic opportunity advertisers.
                elif current_advertiser.advertiser_type == "e":
                    self.no_economic_ads_female += 1
                    self.no_economic_ads_total += 1
                    self.sum_position_economic_female += winning_advertisers.index(current_advertiser)

    # This method optimizes the bidding strategies of the different advertisers in correspondence to each other's estimated click through rates.
    # It is done in correspondence to the balanced bidding.
    def calculate_utilities(self, winning_advertisers, min_price):
        # Initiate a list for the optimized utilities.
        maximized_utilities = []
        # Iterate through the winning advertisers backwards.
        for current_advertiser in reversed(winning_advertisers):
            # Get the advertisers index.
            position_index = winning_advertisers.index(current_advertiser)
            # Check if the advertiser is the last in the list, if so they pay the reserve price (min_price here).
            if position_index == len(winning_advertisers) - 1:
                next_lower_bid = min_price
            # Otherwise get the advertiser on the next lower position and get their bid.
            else:
                next_advertiser = winning_advertisers[position_index+1]
                next_lower_bid = next_advertiser.bid
            # Check if the advertiser is at the first position, if so they bid truthfully, since they pay the next lower bid.
            if position_index == 0:
                best_bid = current_advertiser.estimated_value
            # Otherwise calculate the optimized bid by the balanced bidding equation:
            # value_i - (pos_i/pos_(i-1) * (value_i - value_(i+1)), where i = current advertiser
            else:
                best_bid = current_advertiser.estimated_value - (self.position_effects[position_index]/self.position_effects[position_index-1] * (current_advertiser.estimated_value - next_lower_bid))
            # Set the best bid as the effective bid for the advertiser
            current_advertiser.set_bid(best_bid)
            # Append the best bid to the to the maximized utility list.
            maximized_utilities.append(best_bid)
        # Reverse the list to get the same order as for the winning advertisers.
        maximized_utilities.sort(reverse=True)
        # Return the list.
        return maximized_utilities

    # Calculate the average slot positions for ads of a certain type shown to users of a certain type.
    def calculate_avg_positions(self):
        # Check if there are any retail ads shown to male users in the current simulations
        # If not the average position is 0 --> N\A
        if self.no_retail_ads_male == 0:
            self.avg_position_retail_male = 0
        # Otherwise divide the sum of all position of male shown retail ads by the total number of retail ads shown to male (just average it).
        else:
            self.avg_position_retail_male = self.sum_position_retail_male / self.no_retail_ads_male

        # Check if there are any economic opportunity ads shown to male users in the current simulations
        # If not the average position is 0 --> N\A
        if self.no_economic_ads_male == 0:
            self.avg_position_economic_male = 0
        # Otherwise divide the sum of all position of male shown economic opportunity ads by the total number of economic opportunity ads shown to male (just average it).
        else:
            self.avg_position_economic_male = self.sum_position_economic_male / self.no_economic_ads_male

        # Same procedure for female users:
        # Check if there are any retail ads shown to female users in the current simulations
        # If not the average position is 0 --> N\A
        if self.no_retail_ads_female == 0:
            self.avg_position_retail_female = 0
        # Otherwise divide the sum of all position of female shown retail ads by the total number of retail ads shown to female (just average it).
        else:
            self.avg_position_retail_female = self.sum_position_retail_female / self.no_retail_ads_female

        # Check if there are any economic opportunity ads shown to female users in the current simulations
        # If not the average position is 0 --> N\A
        if self.no_economic_ads_female == 0:
            self.avg_position_economic_female = 0
        # Otherwise divide the sum of all position of female shown economic opportunity ads by the total number of economic opportunity ads shown to female (just average it).
        else:
            self.avg_position_economic_female = self.sum_position_economic_female / self.no_economic_ads_female

    # Count the total number of advertisers by their type
    def count_advertisers(self):
        # Iterate through all advertisers.
        for current_advertiser in self.advertisers:
            # Count the corresponding types.
            if current_advertiser.advertiser_type == "r":
                self.no_retailer += 1
            elif current_advertiser.advertiser_type == "e":
                self.no_economic += 1
        return
