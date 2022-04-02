import numpy as np
import random
import auction


class SimulationStatistics:
    """
    This class keeps the statistics for one run/seed of the experiment
      (i.e. one population sample).
    Each will consist of a vector that catches the metric at each iteration.
    """
    # TODO: Write down what I want to measure.
    # TODO: Maybe track additional values?
    # TODO: @Stefania: Why separate statistics and class itself? How does it work?
    def __init__(self, no_iterations):
        self.no_iterations = no_iterations

        # number of retailer and economic opportunity advertisers at each iteration
        self.no_retailer = np.zeros(no_iterations)
        self.no_economic = np.zeros(no_iterations)

        # number of female and male users at each iteration
        self.no_female = np.zeros(no_iterations)
        self.no_male = np.zeros(no_iterations)

        # number of retail ads shown to female and male users at each iteration
        self.no_retail_ads_female = np.zeros(no_iterations)
        self.no_retail_ads_male = np.zeros(no_iterations)

        # number of economic opportunity ads shown to female and male users at each iteration
        self.no_economic_ads_female = np.zeros(no_iterations)
        self.no_economic_ads_male = np.zeros(no_iterations)

        # platform revenue
        self.platform_revenue = np.zeros(no_iterations)

    # TODO: Maybe removable?! @Stefania
    def divide_by(self, no_samples):
        """Divides all the numbers by the no_samples.
        Useful for taking average statistics"""

        self.no_retailer /= no_samples
        self.no_economic /= no_samples

        # number of female and male users at each iteration
        self.no_female /= no_samples
        self.no_male /= no_samples

        # number of retail ads shown to female and male users at each iteration
        self.no_retail_ads_female /= no_samples
        self.no_retail_ads_male /= no_samples

        # number of economic opportunity ads shown to female and male users at each iteration
        self.no_economic_ads_female /= no_samples
        self.no_economic_ads_male /= no_samples

        # platform revenue
        self.platform_revenue /= no_samples

    def add_values(self, other_stats):
        """ Adds the values of another statistics component-wise."""

        self.no_retailer += other_stats.no_retailer
        self.no_economic += other_stats.no_economic

        # number of female and male users at each iteration
        self.no_female += other_stats.no_female
        self.no_male += other_stats.no_male

        # number of retail ads shown to female and male users at each iteration
        self.no_retail_ads_female += other_stats.no_retail_ads_female
        self.no_retail_ads_male += other_stats.no_retail_ads_male

        # number of economic opportunity ads shown to female and male users at each iteration
        self.no_economic_ads_female += other_stats.no_economic_ads_female
        self.no_economic_ads_male += other_stats.no_economic_ads_male

        # platform revenue
        self.platform_revenue += other_stats.platform_revenue


class SingleSimulation:
    """ This class contains parameters and corresponding statistics."""

    # Define all import properties for a single simulation.
    def __init__(self, list_parameters):

        # Save the parameters to pass it to the individual classes!
        self.parameters = list_parameters

        # Save the number of iterations to calculate the mean from the simulations.
        no_iterations = int(list_parameters['no_iterations'])

        # Generate the corresponding statistics to the simulations.
        self.statistics = SimulationStatistics(no_iterations)

    def add_values(self, other):
        self.statistics.add_values(other.statistics)

    def divide_by(self, no_samples):
        self.statistics.divide_by(no_samples)

    # TODO: Maybe discard this for my simulation?
    def get_different_parameters(self, other_sim):
        """Returns a list with the names of the parameters that are different
        between the current simulation and another simulation (other_sim)."""

        differences = []
        for param_name in self.parameters.keys():
            if self.parameters[param_name] != other_sim.parameters[param_name]:
                differences += [param_name]

        return differences

    def get_stats(self, show_progress=True):
        """Runs the simulation with the given parameters."""

        # read simulation parameters
        no_iterations = int(self.parameters['no_iterations'])
        random_seed = int(self.parameters['random_seed'])

        # TODO: @Stefania why both?
        random.seed(random_seed)
        np.random.seed(random_seed)

        for i in range(no_iterations):
            if show_progress:
                print('Seed ', random_seed, '--- iteration ', i)

            # generate a new auction
            single_auction = auction.Auction(self.parameters)
            single_auction.generate_users(single_auction.user_size)
            single_auction.generate_advertisers(single_auction.advertiser_size)
            single_auction.bidding()

            # update the statistics
            self.statistics.no_male[i] = single_auction.no_male
            self.statistics.no_female[i] = single_auction.no_female
            self.statistics.no_retailer[i] = single_auction.no_retailer
            self.statistics.no_economic[i] = single_auction.no_economic

            self.statistics.no_retail_ads_male[i] = single_auction.no_retail_ads_male
            self.statistics.no_retail_ads_female[i] = single_auction.no_retail_ads_female
            self.statistics.no_economic_ads_male[i] = single_auction.no_economic_ads_male
            self.statistics.no_economic_ads_female[i] = single_auction.no_economic_ads_female

            self.statistics.platform_revenue = single_auction.platform_revenue

        # graph.Graph.drawAdPerSexHistogram(graph, self.retail_ads_male,
        #                           self.retail_ads_female,
        #                           self.economic_ads_male,
        #                           self.economic_ads_female)
