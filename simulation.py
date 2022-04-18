import numpy as np

import proportional_slot_auction
import unrestrained_gsp_auction


class SingleSimulation:
    """ This class contains parameters and corresponding statistics."""

    # Define all import properties for a single simulation.
    def __init__(self, list_parameters):
        # Save the parameters to pass it to the individual classes!
        self.parameters = list_parameters

    def get_stats(self):
        """Runs the simulation with the given parameters."""

        # read simulation parameters
        random_seed = [98188, 66162, 13363, 13235, 36248,
                       15, 62692, 7892, 90537, 14756,
                       72934, 67102, 52, 6784, 96430,
                       79216, 88064, 68301, 57192, 4745,
                       5719, 4143, 63913, 66113, 98683]
        result_1 = []
        result_2 = []

        # iterate through the seeds
        for seed in random_seed:
            np.random.seed(seed)
            print("Seed", seed)
            # generate a unrestrained gsp auction
            auction_1 = unrestrained_gsp_auction.Auction(self.parameters)
            users = auction_1.generate_users(auction_1.user_size)
            advertisers = auction_1.generate_advertisers(auction_1.advertiser_size)

            # generate a separated slot auction
            auction_2 = proportional_slot_auction.Auction(self.parameters)
            auction_2.set_users(users.copy())
            auction_2.set_advertisers(advertisers.copy())

            # run the unrestrained gsp auction
            auction_1.auctioning()

            # run the separated proportional slot gsp auction
            auction_2.reset_advertisers_budget()
            auction_2.auctioning()

            # update the statistics
            # [no male, no female, no retail advertiser, no economic advertiser,
            # no retailer ads total, no economic ads total,
            # no retail ads male, no retail ads female, no economic ads male, no economic ads female,
            # average position male retail, average position male economic, average position female retail, average position female economic,
            # platform revenue]

            result_1.extend(self.update_statistics(auction_1))
            result_2.extend(self.update_statistics(auction_2))

        return result_1, result_2

    def update_statistics(self, auction):
        result = []
        percentage_retail_ads_male = 0
        if auction.no_retail_ads_total != 0:
            percentage_retail_ads_male = auction.no_retail_ads_male / auction.no_retail_ads_total

        per_user_retail_ads_male = 0
        if auction.no_male != 0:
            per_user_retail_ads_male = auction.no_retail_ads_male / auction.no_male

        result.append(["male", auction.no_retail_ads_male, percentage_retail_ads_male,
                       per_user_retail_ads_male, "retailer", auction.avg_position_retail_male,
                       auction.no_male, auction.no_female, auction.no_retailer,
                       auction.no_economic, auction.platform_revenue[0],
                       self.parameters["ratio_sex_users"], self.parameters["ratio_advertisers"],
                       self.parameters["budget"],
                       self.parameters["ratio_user_advertiser"], self.parameters["advertiser_size"]])

        percentage_retail_ads_female = 0
        if auction.no_retail_ads_total != 0:
            percentage_retail_ads_female = auction.no_retail_ads_female / auction.no_retail_ads_total

        per_user_retail_ads_female = 0
        if auction.no_female != 0:
            per_user_retail_ads_female = auction.no_retail_ads_female / auction.no_female

        result.append(["female", auction.no_retail_ads_female, percentage_retail_ads_female,
                       per_user_retail_ads_female, "retailer", auction.avg_position_retail_female])

        percentage_economic_ads_male = 0
        if auction.no_economic_ads_total != 0:
            percentage_economic_ads_male = auction.no_economic_ads_male / auction.no_economic_ads_total

        per_user_economic_ads_male = 0
        if auction.no_male != 0:
            per_user_economic_ads_male = auction.no_economic_ads_male / auction.no_male

        result.append(["male", auction.no_economic_ads_male, percentage_economic_ads_male,
                       per_user_economic_ads_male, "economic", auction.avg_position_economic_male])

        percentage_economic_ads_female = 0
        if auction.no_economic_ads_total != 0:
            percentage_economic_ads_female = auction.no_economic_ads_female / auction.no_economic_ads_total

        per_user_economic_ads_female = 0
        if auction.no_female != 0:
            per_user_economic_ads_female = auction.no_economic_ads_female / auction.no_female

        result.append(["female", auction.no_economic_ads_female, percentage_economic_ads_female,
                       per_user_economic_ads_female, "economic", auction.avg_position_economic_female])

        return result


def write_header():
    header = ["sex", "absolute", "percentage", "ratio per user", "type", "avg position",
              "no_male", "no_female", "no_retailer", "no_economic", "platform revenue",
              "ratio_sex_users", "ratio_advertisers", "budget", "ratio_user_advertiser", "advertiser_size"]
    return header
