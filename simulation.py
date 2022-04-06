import numpy as np
import auction
import graph


class SingleSimulation:
    """ This class contains parameters and corresponding statistics."""

    # Define all import properties for a single simulation.
    def __init__(self, list_parameters):
        # Save the parameters to pass it to the individual classes!
        self.parameters = list_parameters

        self.output = []

    def get_stats(self, show_progress=True):
        """Runs the simulation with the given parameters."""

        # read simulation parameters
        random_seed = int(self.parameters['random_seed'])

        np.random.seed(random_seed)

        # generate a new auction
        single_auction = auction.Auction(self.parameters)
        single_auction.generate_users(single_auction.user_size)
        single_auction.generate_advertisers(single_auction.advertiser_size)
        single_auction.auctioning()

        # update the statistics
        self.output.append(["no male", single_auction.no_male])
        self.output.append(["no female", single_auction.no_female])
        self.output.append(["no retailer", single_auction.no_retailer])
        self.output.append(["no economic", single_auction.no_economic])

        self.output.append(["no retail ads male", single_auction.no_retail_ads_male])
        self.output.append(["no retail ads female", single_auction.no_retail_ads_female])
        self.output.append(["no economic ads male", single_auction.no_economic_ads_male])
        self.output.append(["no economic ads female", single_auction.no_economic_ads_female])

        self.output.append(["average position male retail", single_auction.avg_position_retail_male])
        self.output.append(["average position male economic", single_auction.avg_position_economic_male])
        self.output.append(["average position female retail", single_auction.avg_position_retail_female])
        self.output.append(["average position female economic", single_auction.avg_position_economic_female])

        self.output.append(["platform revenue", single_auction.platform_revenue[0]])

        # TODO: Save solutions into a csv format and open it with seafile?
        self.generate_graph(single_auction.no_retail_ads_male, single_auction.no_retail_ads_female, single_auction.no_economic_ads_male, single_auction.no_economic_ads_female)

    def generate_graph(self, no_retail_ads_male, no_retail_ads_female, no_economic_ads_male, no_economic_ads_female):

        # TODO: Generate Graph!
        graph.Graph.draw_ad_per_sex_hist(graph, no_retail_ads_male, no_retail_ads_female, no_economic_ads_male, no_economic_ads_female, )
