import numpy as np
import separated_slots_auction
import unrestrained_auction

"""
This class makes multiple auction for one config file with multiple seeds.
It then saves the statistics into a result list with and provides a header to save the output into a useful csv.
"""


class SingleSimulation:

    # Define all important properties for a single simulation.
    def __init__(self, list_parameters):
        # Save the parameters to pass it to the individual classes!
        self.parameters = list_parameters

    def get_stats(self):
        """Runs the simulation with the given parameters."""

        # This list of random_seeds should be adjusted based on the size of the users and advertisers to reduce the runtime.
        # TODO: Make the size of the random seeds dynamic.
        random_seed = [98188, 66162, 13363, 13235, 36248,
                       15, 62692, 7892, 90537, 14756,
                       72934, 67102, 52, 6784, 96430,
                       79216, 88064, 68301, 57192, 4745,
                       5719, 4143, 63913, 66113, 98683]
        # Have two result list for the separated slots auction and the unrestrained gsp auction.
        result_1 = []
        result_2 = []

        # Iterate through the seeds and run for each an unrestrained and a separated slots auction.
        for seed in random_seed:
            np.random.seed(seed)
            # Print statement to visualize the progress.
            print("Seed", seed)

            # Generate a unrestrained gsp auction.
            auction_1 = unrestrained_auction.Unrestrained_Auction(self.parameters)
            # Generate the users.
            users = auction_1.generate_users(auction_1.user_size)
            # Generate the advertisers.
            advertisers = auction_1.generate_advertisers(auction_1.advertiser_size)

            # Generate a separated slot auction.
            auction_2 = separated_slots_auction.Separated_Slots_Auction(self.parameters)
            # Copy the users of the unrestrained auction to use the same set.
            auction_2.set_users(users.copy())
            # Copy the advertisers of the unrestrained auction to use the same set.
            auction_2.set_advertisers(advertisers.copy())

            # Run the unrestrained gsp auction.
            auction_1.auctioning()

            # Reset the advertisers' budgets.
            auction_2.reset_advertisers_budget()
            # Run the separated slots gsp auction.
            auction_2.auctioning()

            # Update the output statistics.
            result_1.extend(self.update_statistics(auction_1))
            result_2.extend(self.update_statistics(auction_2))

        # Return the results for both auctions.
        return result_1, result_2

    # This method save the statistic of one auction into a result list.
    def update_statistics(self, auction):
        # Initialize the result list.
        result = []
        # Initialize the percentage of retail ads shown to male users.
        percentage_retail_ads_male = 0
        # Check if the number of retail ads is not zero
        if auction.no_retail_ads_total != 0:
            # If so divide the number of retail ads shown to male users by the total number of retail ads shown to users.
            percentage_retail_ads_male = auction.no_retail_ads_male / auction.no_retail_ads_total

        # This statistic is not useful and had an error in the previous simulation
        # It is unused during the evaluation of the statistics.
        # TODO: Rerun the simulations and check if the numbers are correct.
        # Initialize the ratio of retail ads seen by male users in average
        per_user_retail_ads_male = 0
        # Check if there are male users.
        if auction.no_male != 0:
            # If so divide the number of retail ads shown to male users by the total number of male users.
            per_user_retail_ads_male = auction.no_retail_ads_male / auction.no_male

        # Append to the results a line with the statistics for retail advertisers and :
        # The number of female & male users.
        # The number of retail and economic opportunity advertisers.
        # The platform revenue.
        # The used configurations for the simulation.
        result.append(["male", auction.no_retail_ads_male, percentage_retail_ads_male,
                       per_user_retail_ads_male, "retailer", auction.avg_position_retail_male,
                       auction.no_male, auction.no_female, auction.no_retailer,
                       auction.no_economic, auction.platform_revenue[0],
                       self.parameters["ratio_sex_users"], self.parameters["ratio_advertisers"],
                       self.parameters["budget"],
                       self.parameters["ratio_user_advertiser"], self.parameters["advertiser_size"]])

        # Same procedure for female users and retail ads.
        # Initialize the percentage of retail ads shown to female users.
        percentage_retail_ads_female = 0
        # Check if the number of retail ads is not zero.
        if auction.no_retail_ads_total != 0:
            # If so divide the number of retail ads shown to female users by the total number of retail ads shown to users.
            percentage_retail_ads_female = auction.no_retail_ads_female / auction.no_retail_ads_total

        # Initialize the ratio of retail ads seen by female users in average.
        per_user_retail_ads_female = 0
        # Check if there are female users.
        if auction.no_female != 0:
            # If so divide the number of retail ads shown to female users by the total number of female users.
            per_user_retail_ads_female = auction.no_retail_ads_female / auction.no_female

        # Append to the results a line with the statistics for retail advertisers.
        result.append(["female", auction.no_retail_ads_female, percentage_retail_ads_female,
                       per_user_retail_ads_female, "retailer", auction.avg_position_retail_female])

        # Same procedure for male users and economic opportunity ads.
        # Initialize the percentage of economic opportunity ads shown to male users.
        percentage_economic_ads_male = 0
        # Check if the number of economic opportunity ads is not zero.
        if auction.no_economic_ads_total != 0:
            # If so divide the number of retail ads shown to male users by the total number of economic opportunity ads shown to users.
            percentage_economic_ads_male = auction.no_economic_ads_male / auction.no_economic_ads_total

        # Initialize the ratio of economic opportunity ads seen by male users in average.
        per_user_economic_ads_male = 0
        # Check if there are male users.
        if auction.no_male != 0:
            # If so divide the number of economic opportunity ads shown to male users by the total number of male users.
            per_user_economic_ads_male = auction.no_economic_ads_male / auction.no_male

        # Append to the results a line with the statistics for economic opportunity advertisers.
        result.append(["male", auction.no_economic_ads_male, percentage_economic_ads_male,
                       per_user_economic_ads_male, "economic", auction.avg_position_economic_male])

        # Same procedure for female users and economic opportunity ads.
        # Initialize the percentage of economic opportunity ads shown to female users.
        percentage_economic_ads_female = 0
        # Check if the number of economic opportunity ads is not zero.
        if auction.no_economic_ads_total != 0:
            # If so divide the number of economic opportunity ads shown to female users by the total number of economic opportunity ads shown to users.
            percentage_economic_ads_female = auction.no_economic_ads_female / auction.no_economic_ads_total

        # Initialize the ratio of economic opportunity ads seen by female users in average.
        per_user_economic_ads_female = 0
        # Check if there are female users.
        if auction.no_female != 0:
            # If so divide the number of economic opportunity ads shown to female users by the total number of female users.
            per_user_economic_ads_female = auction.no_economic_ads_female / auction.no_female

        # Append to the results a line with the statistics for economic opportunity advertisers.
        result.append(["female", auction.no_economic_ads_female, percentage_economic_ads_female,
                       per_user_economic_ads_female, "economic", auction.avg_position_economic_female])

        # return the nested result list. Each sublist corresponds to a row in the csv.
        return result


# This method writes the header of the csv file --> it names the columns correctly.
def write_header():
    header = ["sex", "absolute", "percentage", "ratio per user", "type", "avg position",
              "no_male", "no_female", "no_retailer", "no_economic", "platform revenue",
              "ratio_sex_users", "ratio_advertisers", "budget", "ratio_user_advertiser", "advertiser_size"]
    return header
