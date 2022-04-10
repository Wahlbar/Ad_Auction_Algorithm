import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os


def ad_per_sex_bar_plot(data_frame):
    figure = sns.catplot(
        data=data_frame, kind="bar",
        x="type", y="absolute", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6
    )
    plt.show()
    return


def draw_multiple():
    """Runs a simulation for each parameter combination file listed in file_name
    File_name should have multiple lines, each with a "VariablesXXXXX.csv" """
    # folder path
    dir_path = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results"
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1

    for i in range(count):
        print("Graph: ", i+1)
        with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Data" + str(i+1) + ".csv",
                  'w') as document:
            data_frame = pd.read_csv(document)
            ad_per_sex_bar_plot(data_frame)

    return


draw_multiple()


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
