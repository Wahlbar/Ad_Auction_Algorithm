import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os


def ad_per_sex_bar_plot_absolute(data_frame, no, folder):
    ratio_sex_users = int(data_frame["ratio_sex_users"].values[0] * 100)
    ratio_advertisers = int(data_frame["ratio_advertisers"].values[0] * 100)
    budget = int(data_frame["budget"].values[0])
    advertiser_size = int(data_frame["advertiser_size"].values[0])
    user_size = int(data_frame["ratio_user_advertiser"].values[0]) * advertiser_size

    figure = sns.catplot(
        data=data_frame, kind="bar",
        x="type", y="absolute", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6
    )

    (figure.set_axis_labels("Advertiser Type", "Number of Slots Won")
     .set_xticklabels(["Retail", "Economic Opportunity"]))
    # plt.title("Absolute number of retail and economic ads shown to male and female users")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.1, "female to male ratio: " + str(ratio_sex_users) + "%\n"
                             "retailer to economic opportunity ratio: " + str(ratio_advertisers) + "%\n"
                             "advertiser size: " + str(advertiser_size) + "\n"
                             "user size: " + str(user_size) + "\n"
                             "budget: " + str(budget) + "\n", fontsize=10, bbox=props)

    plt.savefig(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Graph" + folder + "catplot_absolute" + str(
        no) + ".jpg", bbox_inches='tight')
    plt.close()
    return


def ad_per_sex_bar_plot_percentage(data_frame, no, folder):
    ratio_sex_users = int(data_frame["ratio_sex_users"].values[0] * 100)
    ratio_advertisers = int(data_frame["ratio_advertisers"].values[0] * 100)
    budget = int(data_frame["budget"].values[0])
    advertiser_size = int(data_frame["advertiser_size"].values[0])
    user_size = int(data_frame["ratio_user_advertiser"].values[0]) * advertiser_size

    figure = sns.catplot(
        data=data_frame, kind="bar",
        x="type", y="percentage", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6, legend_out=True)

    (figure.set_axis_labels("Advertiser Type", "Percentage of Auctions Won")
     .set_xticklabels(["Retail", "Economic Opportunity"])
     .set(ylim=(0, 1)))
    # plt.title("Percentage of retail and economic ads shown to male and female users")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.1, "female to male ratio: " + str(ratio_sex_users) + "%\n"
                             "retailer to economic opportunity ratio: " + str(ratio_advertisers) + "%\n"
                             "advertiser size: " + str(advertiser_size) + "\n"
                             "user size: " + str(user_size) + "\n"
                             "budget: " + str(budget) + "\n", fontsize=10, bbox=props)

    # plt.show()
    plt.savefig(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Graph" + folder + "catplot_percentage" + str(
        no) + ".jpg", bbox_inches='tight')
    plt.close()
    return


def draw_multiple():
    """Runs a simulation for each parameter combination file listed in file_name
    File_name should have multiple lines, each with a "VariablesXXXXX.csv" """
    # folder path
    dir_path_unrestrained = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\unrestrained"
    count = 0
    folder_unrestrained = "/unrestrained/"
    # Iterate directory
    for path in os.listdir(dir_path_unrestrained):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path_unrestrained, path)):
            count += 1

    count = 1
    for i in range(count):
        print("Graph: ", i + 1)
        with open(dir_path_unrestrained + r"\Data" + str(i + 1) + ".csv",
                  'r') as document:
            data_frame = pd.read_csv(document)
            ad_per_sex_bar_plot_absolute(data_frame, i + 1, folder_unrestrained)
            ad_per_sex_bar_plot_percentage(data_frame, i + 1, folder_unrestrained)

    dir_path_prop_slot = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\prop_slot"
    count = 0
    folder_prop_slot = "/prop_slot/"
    # Iterate directory
    for path in os.listdir(dir_path_prop_slot):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path_prop_slot, path)):
            count += 1

    count = 1
    for i in range(count):
        print("Graph: ", i + 1)
        with open(dir_path_prop_slot + r"\Data" + str(i + 1) + ".csv",
                  'r') as document:
            data_frame = pd.read_csv(document)
            ad_per_sex_bar_plot_absolute(data_frame, i + 1, folder_prop_slot)
            ad_per_sex_bar_plot_percentage(data_frame, i + 1, folder_prop_slot)
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
