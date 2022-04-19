import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os


def add_type_to_set(data_frame, auction_type):
    type_column = []
    for i in range(0, len(data_frame)):
        type_column.append(auction_type)

    data_frame.insert(loc=0, column="Auction Type", value=type_column)
    return data_frame


def average_revenue(data_frame, auction_type):
    df_average_revenue = data_frame[
        ["platform revenue", "ratio_sex_users", "ratio_advertisers", "budget", "ratio_user_advertiser",
         "advertiser_size"]]
    clean_df_average_revenue = df_average_revenue.dropna()

    revenue_average = clean_df_average_revenue["platform revenue"].describe()["mean"]
    revenue_std = clean_df_average_revenue["platform revenue"].describe()["std"]
    ratio_sex_users = float(data_frame["ratio_sex_users"].values[0])
    ratio_advertisers = float(data_frame["ratio_advertisers"].values[0])
    budget = int(data_frame["budget"].values[0])
    ratio_user_advertiser = int(data_frame["ratio_user_advertiser"].values[0])
    advertiser_size = int(data_frame["advertiser_size"].values[0])

    return [revenue_average, revenue_std, ratio_sex_users, ratio_advertisers, budget,
            ratio_user_advertiser, advertiser_size, auction_type]


def combine_dataframes(data_frame_1, data_frame_2, type_1, type_2):
    ratio_sex_users = int(data_frame_1["ratio_sex_users"].values[0] * 100)
    ratio_advertisers = int(data_frame_1["ratio_advertisers"].values[0] * 100)
    budget = int(data_frame_1["budget"].values[0])
    advertiser_size = int(data_frame_1["advertiser_size"].values[0])
    user_size = int(data_frame_1["ratio_user_advertiser"].values[0]) * advertiser_size

    variables = [ratio_sex_users, ratio_advertisers, budget, advertiser_size, user_size]
    data_frame_1 = add_type_to_set(data_frame_1, type_1)
    data_frame_2 = add_type_to_set(data_frame_2, type_2)

    total = pd.concat([data_frame_1, data_frame_2], ignore_index=True)
    return total, variables


def ad_per_sex_bar_plot_absolute(dataframe, variables, no, folder):
    figure = sns.catplot(
        data=dataframe, kind="bar",
        x="type", y="absolute", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6, col="Auction Type", legend_out=True
    )

    (figure.set_axis_labels("Advertiser Type", "Number of Slots Won")
     .set_xticklabels(["Retail", "Economic Opportunity"]))
    # plt.title("Absolute number of retail and economic ads shown to male and female users")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.8,
                   "Female to Male Ratio: " + str(variables[0]) + "%\n"
                   "Retailer to Economic Opportunity Ratio: " + str(variables[1]) + "%\n"
                   "Advertiser Size: " + str(variables[3]) + "\n"
                   "User Size: " + str(variables[4]) + "\n"
                   "Budget: " + str(variables[2]) + "\n",
                   fontsize=10, bbox=props)

    # iterate through the axes containers
    for ax in figure.axes.ravel():

        # add annotations
        for c in ax.containers:
            labels = [f'{(int(v.get_height()))}' for v in c]
            ax.bar_label(c, labels=labels, label_type='center')
        ax.margins(y=0.2)
    plt.savefig(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/" + folder + "/catplot_absolute" + str(
            no) + ".jpg", bbox_inches='tight')
    plt.close()
    return


def ad_per_sex_bar_plot_percentage(dataframe, variables, no, folder):
    figure = sns.catplot(
        data=dataframe, kind="bar",
        x="type", y="percentage", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6, legend_out=True, col="Auction Type")

    (figure.set_axis_labels("Advertiser Type", "Percentage of Auctions Won")
     .set_xticklabels(["Retail", "Economic Opportunity"])
     .set(ylim=(0, 1)))
    # plt.title("Percentage of retail and economic ads shown to male and female users")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.8,
                   "Female to Male Ratio: " + str(variables[0]) + "%\n"
                   "Retailer to Economic Opportunity Ratio: " + str(variables[1]) + "%\n"
                   "Advertiser Size: " + str(variables[3]) + "\n"
                   "User Size: " + str(variables[4]) + "\n"
                   "Budget: " + str(variables[2]) + "\n",
                   fontsize=10, bbox=props)

    # iterate through the axes containers
    for ax in figure.axes.ravel():

        # add annotations
        for c in ax.containers:
            labels = [f'{(v.get_height()):.2f}' for v in c]
            ax.bar_label(c, labels=labels, label_type='center')
        ax.margins(y=0.2)
    plt.savefig(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/" + folder + "/catplot_percentage" + str(
            no) + ".jpg", bbox_inches='tight')
    plt.close()
    return


def draw_multiple():
    """Runs a simulation for each parameter combination file listed in file_name
    File_name should have multiple lines, each with a "VariablesXXXXX.csv" """
    # folder path
    dir_path_unrestrained = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\Unrestrained GSP"
    dir_path_prop_slot = "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/Separated Slots GSP"
    count = 0
    auction_unrestrained = "Unrestrained GSP"
    auction_separated = "Separated Slots GSP"
    folder = "combination"
    # Iterate directory
    for path in os.listdir(dir_path_unrestrained):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path_unrestrained, path)):
            count += 1

    data_frame_unrestrained = pd.DataFrame([],
                                           columns=["platform revenue average", "std", "ratio_sex_users",
                                                    "ratio_advertisers", "budget", "ratio_user_advertiser",
                                                    "advertiser_size", "type"])
    data_frame_prop_slot = pd.DataFrame([],
                                        columns=["platform revenue average", "std", "ratio_sex_users",
                                                 "ratio_advertisers", "budget", "ratio_user_advertiser",
                                                 "advertiser_size", "type"])

    data_frame_total = pd.DataFrame([],
                                    columns=["Auction Type", "sex", "absolute", "percentage", "ratio per user", "type",
                                             "avg position", "no_male", "no_female", "no_retailer", "no_economic",
                                             "platform revenue", "ratio_sex_users", "ratio_advertisers",
                                             "budget", "ratio_user_advertiser", "advertiser_size"
                                             ])

    # count = 1
    for i in range(count):
        print("Graph: ", i + 1)
        with open(dir_path_unrestrained + r"\Data" + str(i + 1) + ".csv",
                  'r') as csv_unrestrained:
            df_unrestrained = pd.read_csv(csv_unrestrained)

        with open(dir_path_prop_slot + r"\Data" + str(i + 1) + ".csv",
                  'r') as csv_separated:
            df_separated = pd.read_csv(csv_separated)

            data_frame_unrestrained.loc[i] = average_revenue(df_unrestrained, auction_unrestrained)
            data_frame_prop_slot.loc[i] = average_revenue(df_separated, auction_separated)

            data_frames_combined, variables = combine_dataframes(df_unrestrained, df_separated, auction_unrestrained,
                                                                 auction_separated)
            data_frame_total = pd.concat([data_frame_total, data_frames_combined], ignore_index=True)
            ad_per_sex_bar_plot_absolute(data_frames_combined, variables, i + 1, folder)
            ad_per_sex_bar_plot_percentage(data_frames_combined, variables, i + 1, folder)

    total = pd.concat([data_frame_unrestrained, data_frame_prop_slot], ignore_index=True)
    total.to_csv(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\total\Data_short.csv")
    data_frame_total.to_csv(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long.csv")
    return


def draw_revenue_graph():
    with open("C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_short.csv") as data:
        dataframe = pd.read_csv(data, index_col=0)
        new_names = {'ratio_user_advertiser': 'User Size',
                     'advertiser_size': 'Advertiser Size',
                     'budget': 'Budget',
                     'ratio_sex_users': 'Female to Male Ratio',
                     'platform revenue average': 'Platform Revenue',
                     'ratio_advertisers': 'Retailer to Economic \n'
                                          'Opportunity Ratio',
                     'type': 'Auction Type',
                     'std': 'Standard Deviation'
                     }

        # call rename () method
        dataframe.rename(columns=new_names, inplace=True)

        user_l_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 100)]
        user_s_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 10) & (dataframe["Advertiser Size"] == 100)]
        user_l_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 10)]
        user_s_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 10) & (dataframe["Advertiser Size"] == 10)]
        sample_sizes = [user_l_advertiser_l, user_s_advertiser_l, user_l_advertiser_s, user_s_advertiser_s]

        user_size = [100, 10, 100, 10]
        advertiser_size = [100, 100, 10, 10]

        colors = ["black", "#003f5c", "#2f4b7c", "#665191", "#a05195",
                  "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]
        population_size = ["user_l_adv_l", "user_s_adv_l", "user_l_adv_s", "user_s_adv_s"]
        i = 0
        for df in sample_sizes:

            bud_100 = df.loc[df["Budget"] == 100]
            bud_1000 = df.loc[df["Budget"] == 1000]
            bud_10000 = df.loc[df["Budget"] == 10000]
            revenue_vs_user_ratio = [bud_100, bud_1000, bud_10000]
            budget_size = 100

            for to_plot in revenue_vs_user_ratio:
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                sns.relplot(
                    data=to_plot, x="Female to Male Ratio", y="Platform Revenue", ci="Standard Deviation", marker='o',
                    err_style="bars", hue="Retailer to Economic \n"
                                          "Opportunity Ratio", col="Auction Type", kind="line",
                    palette=colors
                )
                plt.gcf().text(0.85, 0.85,
                               "Budget: " + str(budget_size) + "\n"
                               "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                               "Advertiser Size: " + str(advertiser_size[i]) + "\n",
                               fontsize=10, bbox=props)

                plt.savefig(
                    "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/revenue to user ratio" + str(
                        budget_size) + population_size[i] + ".jpg", bbox_inches='tight')
                plt.close()

                sns.relplot(
                    data=to_plot, x="Retailer to Economic \n"
                                    "Opportunity Ratio", y="Platform Revenue", ci="Standard Deviation", marker='o',
                    err_style="bars", hue="Female to Male Ratio", col="Auction Type", kind="line",
                    palette=colors
                )
                plt.gcf().text(0.85, 0.85,
                               "Budget: " + str(budget_size) + "\n"
                               "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                               "Advertiser Size: " + str(advertiser_size[i]) + "\n",
                               fontsize=10, bbox=props)

                plt.savefig(
                    "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/revenue to advertiser ratio" + str(
                        budget_size) + population_size[i] + ".jpg", bbox_inches='tight')
                plt.close()
                budget_size *= 10
            i += 1
    return


def draw_percentage_reach_graph():
    with open("C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long_filled.csv") as data:
        dataframe = pd.read_csv(data, index_col=0)
        new_names = {'sex absolute': 'Absolute Number of Ads Seen By User',
                     'sex': 'Sex',
                     'percentage': 'Ratio of Ads Seen By User',
                     'avg position': 'Average Position of the Ad',
                     'no_male': 'Number of Male Users',
                     'no_female': 'Number of Female Users',
                     'no_retailer': 'Number of Retail Advertisers',
                     'no_economic': 'Number of Economic Opportunity Advertisers',

                     'ratio_user_advertiser': 'User Size',
                     'advertiser_size': 'Advertiser Size',
                     'budget': 'Budget',
                     'ratio_sex_users': 'Female to Male Ratio',
                     'platform revenue': 'Platform Revenue',
                     'ratio_advertisers': 'Retailer to Economic \n'
                                          'Opportunity Ratio',
                     'type': 'Advertiser Type'
                     }
        # call rename () method
        dataframe.rename(columns=new_names, inplace=True)

        user_l_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 100)]
        user_l_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 10)]

        sample_sizes = [user_l_advertiser_l, user_l_advertiser_s]

        user_size = [100, 100]
        advertiser_size = [100, 10]
        retail_ratio = [0.9, 0.5, 0.1]

        colors = ["lightblue", "orange"]
        population_size = ["user_l_adv_l", "user_l_adv_s"]

        i = 0

        for df in sample_sizes:

            bud_100 = df.loc[df["Budget"] == 100]
            bud_10000 = df.loc[df["Budget"] == 10000]
            revenue_vs_user_ratio = [bud_100, bud_10000]
            budget_size = 100

            for df2 in revenue_vs_user_ratio:

                retail_ratio_90 = df2.loc[df2['Retailer to Economic \n'
                                              'Opportunity Ratio'] == 0.9]
                retail_ratio_50 = df2.loc[df2['Retailer to Economic \n'
                                              'Opportunity Ratio'] == 0.5]
                retail_ratio_10 = df2.loc[df2['Retailer to Economic \n'
                                              'Opportunity Ratio'] == 0.1]
                user_ratio_90 = df2.loc[df2['Female to Male Ratio'] == 0.9]
                user_ratio_50 = df2.loc[df2['Female to Male Ratio'] == 0.5]
                user_ratio_10 = df2.loc[df2['Female to Male Ratio'] == 0.1]

                user_ratios = [user_ratio_90, user_ratio_50, user_ratio_10]
                advertiser_ratios = [retail_ratio_90, retail_ratio_50, retail_ratio_10]
                ratio = [0.9, 0.5, 0.1]
                for j in range(len(user_ratios)):
                    print("Graph: ", i, ".", budget_size, '.', j)
                    user_ratio = user_ratios[j]
                    advertiser_ratio = advertiser_ratios[j]
                    r = ratio[j]

                    user_ratio = user_ratio.groupby(['Auction Type', 'Sex', 'Advertiser Type', 'Retailer to Economic \n'
                                                                                               'Opportunity Ratio']).agg({'Ratio of Ads Seen By User': ['mean']}).reset_index()
                    user_ratio.columns = ['Auction Type', 'Sex', 'Advertiser Type', 'Retailer to Economic \n'
                                                                                    'Opportunity Ratio', 'Ratio of Ads Seen By User']

                    advertiser_ratio = advertiser_ratio.groupby(['Auction Type', 'Sex', 'Advertiser Type', 'Female to Male Ratio']).agg({'Ratio of Ads Seen By User': ['mean']}).reset_index()
                    advertiser_ratio.columns = ['Auction Type', 'Sex', 'Advertiser Type', 'Female to Male Ratio', 'Ratio of Ads Seen By User']

                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    sns.relplot(
                        data=advertiser_ratio, x="Female to Male Ratio", y="Ratio of Ads Seen By User",
                        hue="Sex", style="Advertiser Type", col="Auction Type", kind="line", ci='sd', marker='o',
                        palette=colors
                    )
                    plt.gcf().text(0.9, 0.8,
                                   "Budget: " + str(budget_size) + "\n"
                                   "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                                   "Advertiser Size: " + str(advertiser_size[i]) + "\n"
                                   "Retailer to Economic Opportunity Ratio: " + str(retail_ratio[j] * 100) + "%\n",
                                   fontsize=10, bbox=props)

                    plt.savefig(
                        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/percentage to user ratio" + str(
                            budget_size) + population_size[i] + "adv_ratio" + str(r) + ".jpg", bbox_inches='tight')
                    plt.close()

                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    sns.relplot(
                        data=user_ratio, x='Retailer to Economic \n'
                                           'Opportunity Ratio',
                        y="Ratio of Ads Seen By User", hue="Sex", style="Advertiser Type", col="Auction Type", kind="line", ci='sd', marker='o',
                        palette=colors
                    )
                    plt.gcf().text(0.9, 0.8,
                                   "Budget: " + str(budget_size) + "\n"
                                   "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                                   "Advertiser Size: " + str(advertiser_size[i]) + "\n"
                                   "Female to Male Ratio: " + str(retail_ratio[j] * 100) + "%\n",
                                   fontsize=10, bbox=props)

                    plt.savefig(
                        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/percentage to advertiser ratio" + str(
                            budget_size) + population_size[i] + "user_ratio" + str(r) + ".jpg", bbox_inches='tight')
                    plt.close()

                budget_size *= 100
            i += 1
    return


def complete_data_frame():
    with open("C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long.csv", 'r') as data:
        dataframe = pd.read_csv(data, index_col=0)
        print("inserting")
        for i in range(0, len(dataframe), 4):
            print("take: ", i)
            for j in range(i+1, i+4):
                print("insert: ", j)
                dataframe.iloc[j, 7] = dataframe.iloc[i, 7]
                dataframe.iloc[j, 8] = dataframe.iloc[i, 8]
                dataframe.iloc[j, 9] = dataframe.iloc[i, 9]
                dataframe.iloc[j, 10] = dataframe.iloc[i, 10]
                dataframe.iloc[j, 11] = dataframe.iloc[i, 11]
                dataframe.iloc[j, 12] = dataframe.iloc[i, 12]
                dataframe.iloc[j, 13] = dataframe.iloc[i, 13]
                dataframe.iloc[j, 14] = dataframe.iloc[i, 14]
                dataframe.iloc[j, 15] = dataframe.iloc[i, 15]
                dataframe.iloc[j, 16] = dataframe.iloc[i, 16]
            i += 4

        dataframe.to_csv(
            "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long_filled.csv")


# draw_multiple()
#




draw_percentage_reach_graph()

