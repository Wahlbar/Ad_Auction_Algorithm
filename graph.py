import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Graph:
    def __init__(self):
        return

    def draw_ad_per_sex_hist(self, no_retail_ads_male, no_retail_ads_female, no_economic_ads_male,
                             no_economic_ads_female):
        # TODO: Ask Stefania about seaborn, error calculation, file types, etc.
        # sns.barplot([no_retail_ads_male, no_retail_ads_female, no_economic_ads_male, no_economic_ads_female])

        labels = ['retail ads - male users', 'retail ads - female users', 'economic ads - male users',
                  'economic ads - female users']
        width = 14
        height = 8
        colors = ['darkblue', 'darkorange', 'blue', 'orange']
        fig, ax = plt.subplots(figsize=(width, height))
        ax.bar(labels, [np.average(no_retail_ads_male), np.average(no_retail_ads_female),
                        np.average(no_economic_ads_male), np.average(no_economic_ads_female)], color=colors)
        plt.title('Ads shown to Female and Male Users')
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.show()

        print(np.average(no_retail_ads_male), np.average(no_retail_ads_female),
              np.average(no_economic_ads_male), np.average(no_economic_ads_female))

    # // TODO: todo
    def draw_revenue_ratio(self):
        return


#################################


    class Simulations:
        """This class contains multiple simulations and makes the relevant plot."""

    def __init__(self, list_parameters):
        # a given list of variables of type simulation
        self.names_parameters = list_parameters[0].parameters.keys()

    def sd(self):
        '''Gets the variance of simulations from the list'''
        no_sim = len(self.list_simulations)
        no_iter = int(self.list_simulations[0].parameters['no_iterations'])

        # find the expected value
        exp = np.zeros(no_iter)
        for s in self.list_simulations:
            # print(s.statistics.percentage_outgroup_long_term[-1])
            exp += s.statistics.percentage_outgroup_long_term
        exp /= no_sim

        # find the variance
        var = 0
        for s in self.list_simulations:
            var += (s.statistics.percentage_outgroup_long_term - exp) ** 2
        var /= no_sim

        return np.sqrt(var)

    def filter(self, param_name, list_param_values):
        '''
        For the value of param_name levaes only the values in the list.
        param_name = string with the name of the parameter we want to filter on
        list_param_values = list with remaining values
        '''

        to_remove = []
        for sim in self.list_simulations:
            if sim.parameters[param_name] not in list_param_values:
                to_remove.append(sim)

        for sim in to_remove:
            self.list_simulations.remove(sim)

    def filter_multiple(self):
        '''Sees the changing parameters and asks wich ones to keep.
        This requires keyboard input.
        '''

        changing_params = self.identify_changing_parameters()
        for param_name in changing_params.keys():
            print("The parameter ", param_name,
                  " is changing with values ", changing_params[param_name])
            print("Do you want to filter these values? [Y/N]")
            filter = input()
            if filter == "Y":
                print("Please list the values you want to remain:")
                list_remain = ast.literal_eval(input())
                self.filter(param_name, list_remain)

    def plot_stats(self, group_by_intn=False):
        '''Plots the relevant statistics depending on the changing parameters
        '''

        cols = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        line_styles = ["-", "--", "-.", ":"]

        def plot_one(simulation, col=-1, line_style="-", add_label=True):
            if add_label:
                label = ''
                for p in changing_params:
                    if p != "norm_intervention":
                        label += p + "=" + simulation.parameters[p] + " | "
            else:
                label = -1
            simulation.statistics.plot_percentage_outgroup_long_term(label, col, line_style)

        # identify the changing parameters
        changing_params = list(self.identify_changing_parameters().keys())

        if not group_by_intn:
            # plot each statistic and add the relevant variable on the legend
            for simulation in self.list_simulations:
                plot_one(simulation, add_label=True)
        else:
            col = 0
            # plot stats with intervention 0-1 in paris, same col
            for sim in self.list_simulations:
                if sim.parameters["norm_intervention"] == '1':
                    col = (col + 1) % len(cols)
                    plot_one(sim, cols[col])
                    for sim_without_intn in self.list_simulations:
                        if sim.get_different_parameters(sim_without_intn) == ["norm_intervention"]:
                            plot_one(sim_without_intn, cols[col], "--", False)

        plt.xlabel('Time')
        plt.ylabel('Percentage of out-group long-term relationships')
        plt.legend()
        plt.show()
