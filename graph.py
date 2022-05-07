import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

'''
This class draws different types of graphs from the output files from the simulations.
'''


# This function adds the auction type (unrestrained, separated slots) to the csv.
# TODO: Maybe extract this method to the main/simulation class and save it already to the output files.
def add_type_to_set(data_frame, auction_type):
    type_column = []
    for i in range(0, len(data_frame)):
        type_column.append(auction_type)

    # Insert the auction type in the first column.
    data_frame.insert(loc=0, column="Auction Type", value=type_column)
    return data_frame


# This method calculates the mean from all multiple seeds in one output file to later save these variables into one csv with all averages.
def average_revenue(data_frame, auction_type):
    # Save the relevant columns.
    df_average_revenue = data_frame[
        ["platform revenue", "ratio_sex_users", "ratio_advertisers", "budget", "ratio_user_advertiser",
         "advertiser_size"]]
    # Clean the empty cells.
    clean_df_average_revenue = df_average_revenue.dropna()

    # Average the platform revenue including the standard deviation
    revenue_average = clean_df_average_revenue["platform revenue"].describe()["mean"]
    revenue_std = clean_df_average_revenue["platform revenue"].describe()["std"]
    # Save the other values as well, but it is not necessary to average them,
    # because they do not change between seeds.
    ratio_sex_users = float(data_frame["ratio_sex_users"].values[0])
    ratio_advertisers = float(data_frame["ratio_advertisers"].values[0])
    budget = int(data_frame["budget"].values[0])
    ratio_user_advertiser = int(data_frame["ratio_user_advertiser"].values[0])
    advertiser_size = int(data_frame["advertiser_size"].values[0])

    # Return the averaged columns
    return [revenue_average, revenue_std, ratio_sex_users, ratio_advertisers, budget,
            ratio_user_advertiser, advertiser_size, auction_type]


# This method combines two dataframes into one.
# It is used to combine two different auction types with the same configurations into one dataframe to then plot both plots together.
def combine_dataframes(data_frame_1, data_frame_2, type_1, type_2):
    # Write the changing config in clean numbers to display then on the detailed legend on the plot.
    ratio_sex_users = int(data_frame_1["ratio_sex_users"].values[0] * 100)
    ratio_advertisers = int(data_frame_1["ratio_advertisers"].values[0] * 100)
    budget = int(data_frame_1["budget"].values[0])
    advertiser_size = int(data_frame_1["advertiser_size"].values[0])
    user_size = int(data_frame_1["ratio_user_advertiser"].values[0]) * advertiser_size

    # Save them all in the dataframe variable.
    variables = [ratio_sex_users, ratio_advertisers, budget, advertiser_size, user_size]
    # Save the auction type to the dataframes.
    data_frame_1 = add_type_to_set(data_frame_1, type_1)
    data_frame_2 = add_type_to_set(data_frame_2, type_2)

    # Combine the dataframes.
    total = pd.concat([data_frame_1, data_frame_2], ignore_index=True)
    return total, variables


# This method draws a bar plot with the absolute number of ads shown to female and male users from retail and ecnomic opportunity advertisers.
def ad_per_sex_bar_plot_absolute(dataframe, variables, no, folder):
    # Create the categorical plot.
    # Errorbar = standard deviation.
    # Divide by sex, advertiser type and auction type.
    figure = sns.catplot(
        data=dataframe, kind="bar",
        x="type", y="absolute", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6, col="Auction Type", legend_out=True
    )

    # Label the axis correct!
    (figure.set_axis_labels("Advertiser Type", "Number of Slots Won")
     .set_xticklabels(["Retail", "Economic Opportunity"]))
    # I removed the title to have a cleaner plot. Plus in the paper, I will add a caption, therefore the title would be redundant.
    # plt.title("Absolute number of retail and economic ads shown to male and female users")
    # Add the detailed configurations as a box on the side of the graph to ease comprehension.
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.8,
                   "Female to Male Ratio: " + str(variables[0]) + "%\n"
                   "Retailer to Economic Opportunity Ratio: " + str(variables[1]) + "%\n"
                   "Advertiser Size: " + str(variables[3]) + "\n"
                   "User Size: " + str(variables[4]) + "\n"
                   "Budget: " + str(variables[2]) + "\n",
                   fontsize=10, bbox=props)

    # This part is to display the exact numbers on the cat plot.
    # Iterate through the axes containers.
    for ax in figure.axes.ravel():

        # Add annotations.
        for c in ax.containers:
            labels = [f'{(int(v.get_height()))}' for v in c]
            ax.bar_label(c, labels=labels, label_type='center')
        ax.margins(y=0.2)
    # Save the figure in the correct folder.
    plt.savefig(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/" + folder + "/catplot_absolute" + str(
            no) + ".jpg", bbox_inches='tight')
    plt.close()
    return

# This method draws a bar plot with the relative number of ads shown to female and male users from retail and ecnomic opportunity advertisers.
def ad_per_sex_bar_plot_percentage(dataframe, variables, no, folder):
    # Create the categorical plot.
    # Errorbar = standard deviation.
    # Divide by sex, advertiser type and auction type.
    figure = sns.catplot(
        data=dataframe, kind="bar",
        x="type", y="percentage", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6, legend_out=True, col="Auction Type")

    # Label the axis correct!
    (figure.set_axis_labels("Advertiser Type", "Percentage of Auctions Won")
     .set_xticklabels(["Retail", "Economic Opportunity"])
     .set(ylim=(0, 1)))
    # I removed the title to have a cleaner plot. Plus in the paper, I will add a caption, therefore the title would be redundant.
    # plt.title("Percentage of retail and economic ads shown to male and female users")
    # Add the detailed configurations as a box on the side of the graph to ease comprehension.
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gcf().text(0.9, 0.8,
                   "Female to Male Ratio: " + str(variables[0]) + "%\n"
                   "Retailer to Economic Opportunity Ratio: " + str(variables[1]) + "%\n"
                   "Advertiser Size: " + str(variables[3]) + "\n"
                   "User Size: " + str(variables[4]) + "\n"
                   "Budget: " + str(variables[2]) + "\n",
                   fontsize=10, bbox=props)

    # This part is to display the exact numbers on the cat plot.
    # Iterate through the axes containers.
    for ax in figure.axes.ravel():

        # Add annotations.
        for c in ax.containers:
            labels = [f'{(v.get_height()):.2f}' for v in c]
            ax.bar_label(c, labels=labels, label_type='center')
        ax.margins(y=0.2)
    # Save the figure in the correct folder.
    plt.savefig(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/" + folder + "/catplot_percentage" + str(
            no) + ".jpg", bbox_inches='tight')
    plt.close()
    return


# This method iterates through the output files of different auctions (unrestrained and separated slots)
# and draws for each an absolute and a relative catplot. (See above.)
def draw_multiple():
    # Folder pathes.
    dir_path_unrestrained = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\Unrestrained GSP"
    dir_path_prop_slot = "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/Separated Slots GSP"
    count = 0
    # Label the types correctly to later display on the graph.
    auction_unrestrained = "Unrestrained GSP"
    auction_separated = "Separated Slots GSP"
    # Save the average in the combination folder.
    folder = "combination"
    # Iterate through the directory.
    for path in os.listdir(dir_path_unrestrained):
        # Check if current path is a file
        if os.path.isfile(os.path.join(dir_path_unrestrained, path)):
            count += 1

    # Generate two empty dataframes with the right columns to add the averages to them
    data_frame_unrestrained = pd.DataFrame([],
                                           columns=["platform revenue average", "std", "ratio_sex_users",
                                                    "ratio_advertisers", "budget", "ratio_user_advertiser",
                                                    "advertiser_size", "type"])
    data_frame_prop_slot = pd.DataFrame([],
                                        columns=["platform revenue average", "std", "ratio_sex_users",
                                                 "ratio_advertisers", "budget", "ratio_user_advertiser",
                                                 "advertiser_size", "type"])

    # Generate an empty dataframe with the all columns to save all dataframes in one big file.
    data_frame_total = pd.DataFrame([],
                                    columns=["Auction Type", "sex", "absolute", "percentage", "ratio per user", "type",
                                             "avg position", "no_male", "no_female", "no_retailer", "no_economic",
                                             "platform revenue", "ratio_sex_users", "ratio_advertisers",
                                             "budget", "ratio_user_advertiser", "advertiser_size"
                                             ])

    # Iterate through all files in both folders, draw the graphs and save the averages.
    for i in range(count):
        print("Graph: ", i + 1)
        with open(dir_path_unrestrained + r"\Data" + str(i + 1) + ".csv",
                  'r') as csv_unrestrained:
            df_unrestrained = pd.read_csv(csv_unrestrained)

        with open(dir_path_prop_slot + r"\Data" + str(i + 1) + ".csv",
                  'r') as csv_separated:
            df_separated = pd.read_csv(csv_separated)

            # Average both dataframes and add them to the average dataframe.
            data_frame_unrestrained.loc[i] = average_revenue(df_unrestrained, auction_unrestrained)
            data_frame_prop_slot.loc[i] = average_revenue(df_separated, auction_separated)

            # Combine both dataframes to one dataframe.
            # TODO: Maybe pull this part out to a different class.
            data_frames_combined, variables = combine_dataframes(df_unrestrained, df_separated, auction_unrestrained,
                                                                 auction_separated)
            # Add both dataframes to the big dataframe, where all results will be saved.
            data_frame_total = pd.concat([data_frame_total, data_frames_combined], ignore_index=True)
            # Draw the plots from the combined dataframe.
            ad_per_sex_bar_plot_absolute(data_frames_combined, variables, i + 1, folder)
            ad_per_sex_bar_plot_percentage(data_frames_combined, variables, i + 1, folder)

    # Save the total averaged dataframe and the complete dataframe to the total folder.
    total = pd.concat([data_frame_unrestrained, data_frame_prop_slot], ignore_index=True)
    total.to_csv(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\total\Data_short.csv")
    data_frame_total.to_csv(
        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long.csv")
    return


# Draw the revenue-to-user-gender-ratio and revenue-to-advertiser-type-ratio graphs from the averaged dataframe.
def draw_revenue_graph():
    # Open the csv and rename the column to get a clean naming in the plot.
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

        # Call rename () method.
        dataframe.rename(columns=new_names, inplace=True)

        # Divide the dataframe by advertiser and user size.
        user_l_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 100)]
        user_s_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 10) & (dataframe["Advertiser Size"] == 100)]
        user_l_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 10)]
        user_s_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 10) & (dataframe["Advertiser Size"] == 10)]
        # Save the divided (sub)dataframes into one list to iterate through.
        sample_sizes = [user_l_advertiser_l, user_s_advertiser_l, user_l_advertiser_s, user_s_advertiser_s]

        # Save the correct user and advertiser size in the same order as the dataframes in the list sample_size.
        user_size = [100, 10, 100, 10]
        advertiser_size = [100, 100, 10, 10]

        # Define a list of different colors to plot 9 different lines in the lineplot. (Used for the revenue.)
        colors = ["black", "#003f5c", "#2f4b7c", "#665191", "#a05195",
                  "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]
        # Define a list with the correct user and size to name and save the figures.
        population_size = ["user_l_adv_l", "user_s_adv_l", "user_l_adv_s", "user_s_adv_s"]
        i = 0
        # Iterate through the dataframe list.
        for df in sample_sizes:

            # Divide the dataframe by budget size and save them into a list.
            bud_100 = df.loc[df["Budget"] == 100]
            bud_1000 = df.loc[df["Budget"] == 1000]
            bud_10000 = df.loc[df["Budget"] == 10000]
            revenue_vs_user_ratio = [bud_100, bud_1000, bud_10000]
            # Define the budget for the first dataframe and multiply it accordingly. (Used for naming again.)
            budget_size = 100

            # Iterate through the dataframe list.
            for to_plot in revenue_vs_user_ratio:
                # Plot a line plot with:
                # x = user gender ratio
                # y = revenue
                # error = standard deviation
                # subplots divided by auction type
                # lines = different retailer to economic opportunity ratio
                # color = color palette defined before
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                sns.relplot(
                    data=to_plot, x="Female to Male Ratio", y="Platform Revenue", ci="Standard Deviation", marker='o',
                    err_style="bars", hue="Retailer to Economic \n"
                                          "Opportunity Ratio", col="Auction Type", kind="line",
                    palette=colors
                )
                # Add a box with the detailed configurations.
                plt.gcf().text(0.85, 0.85,
                               "Budget: " + str(budget_size) + "\n"
                               "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                               "Advertiser Size: " + str(advertiser_size[i]) + "\n",
                               fontsize=10, bbox=props)

                # Save the figure to the folder.
                plt.savefig(
                    "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/revenue to user ratio" + str(
                        budget_size) + population_size[i] + ".jpg", bbox_inches='tight')
                plt.close()

                # Plot a line plot with:
                # x = advertiser type ratio
                # y = revenue
                # error = standard deviation
                # subplots divided by auction type
                # lines = different user gender ratio
                # color = color palette defined before
                sns.relplot(
                    data=to_plot, x="Retailer to Economic \n"
                                    "Opportunity Ratio", y="Platform Revenue", ci="Standard Deviation", marker='o',
                    err_style="bars", hue="Female to Male Ratio", col="Auction Type", kind="line",
                    palette=colors
                )
                # Add a box with the detailed configurations.
                plt.gcf().text(0.85, 0.85,
                               "Budget: " + str(budget_size) + "\n"
                               "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                               "Advertiser Size: " + str(advertiser_size[i]) + "\n",
                               fontsize=10, bbox=props)

                # Save the figure to the folder.
                plt.savefig(
                    "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/revenue to advertiser ratio" + str(
                        budget_size) + population_size[i] + ".jpg", bbox_inches='tight')
                plt.close()

                # Adjust the budget size to not overwrite the previous plots.
                budget_size *= 10
            i += 1
    return


# Draw the percentage of users of different genders reached by different advertiser types in dependence of the user gender ratio and the advertiser type ratio.
def draw_percentage_reach_graph():
    # Open the csv and rename the column to get a clean naming in the plot.
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
        # Call rename () method.
        dataframe.rename(columns=new_names, inplace=True)

        # Divide the dataframe by advertiser and user size.
        # Only select the "higher" user sizes.
        user_l_advertiser_l = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 100)]
        user_l_advertiser_s = dataframe.loc[
            (dataframe["User Size"] == 100) & (dataframe["Advertiser Size"] == 10)]

        # Save the divided (sub)dataframes into one list to iterate through.
        sample_sizes = [user_l_advertiser_l, user_l_advertiser_s]

        # Save the correct user and advertiser size in the same order as the dataframes in the list sample_size
        user_size = [100, 100]
        advertiser_size = [100, 10]

        # Define different advertiser type ratios to draw.
        retail_ratio = [0.9, 0.5, 0.1]

        # Generate the colors for the lineplots.
        colors = ["lightblue", "orange"]

        # Define a list with the correct user and size to name and save the figures.
        population_size = ["user_l_adv_l", "user_l_adv_s"]

        i = 0

        # Iterate through the dataframe list.
        for df in sample_sizes:

            # Divide the dataframe by budget size and save them into a list.
            bud_100 = df.loc[df["Budget"] == 100]
            bud_10000 = df.loc[df["Budget"] == 10000]
            revenue_vs_user_ratio = [bud_100, bud_10000]

            # Define the budget for the first dataframe and multiply it accordingly. (Used for naming again.)
            budget_size = 100

            # Iterate through the new dataframe list.
            for df2 in revenue_vs_user_ratio:

                # Divide the dataframe by advertiser type and user type ratio and save them into two lists.
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
                # Save the ratios.
                ratio = [0.9, 0.5, 0.1]
                # Iterate through one of the list lengths to plot the graphs.
                for j in range(len(user_ratios)):
                    # Print statement to see the progress.
                    print("Graph: ", i, ".", budget_size, '.', j)
                    # Select the first dataframe from the user gender ratio based split and the advertiser type ratio based split as well.
                    user_ratio = user_ratios[j]
                    advertiser_ratio = advertiser_ratios[j]
                    # Select the correct ratio for naming the plot correctly.
                    r = ratio[j]

                    # Group the user dataframe by:
                    # auction type
                    # sex
                    # advertiser type
                    # advertiser ratio
                    # and then average the ratio of ads seen by users
                    user_ratio = user_ratio.groupby(['Auction Type', 'Sex', 'Advertiser Type', 'Retailer to Economic \n'
                                                                                               'Opportunity Ratio']).agg({'Ratio of Ads Seen By User': ['mean']}).reset_index()
                    # Select only the columns user for the grouping and the average. (The rest is irrelevant.)
                    user_ratio.columns = ['Auction Type', 'Sex', 'Advertiser Type', 'Retailer to Economic \n'
                                                                                    'Opportunity Ratio', 'Ratio of Ads Seen By User']

                    # Group the advertiser dataframe by:
                    # auction type
                    # sex
                    # advertiser type
                    # user ratio
                    # and then average the ratio of ads seen by users
                    advertiser_ratio = advertiser_ratio.groupby(['Auction Type', 'Sex', 'Advertiser Type', 'Female to Male Ratio']).agg({'Ratio of Ads Seen By User': ['mean']}).reset_index()
                    # Select only the columns user for the grouping and the average. (The rest is irrelevant.)
                    advertiser_ratio.columns = ['Auction Type', 'Sex', 'Advertiser Type', 'Female to Male Ratio', 'Ratio of Ads Seen By User']

                    # Define the properties for the box with the config informations.
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    # Plot the percentage of ads seen by female and male users in comparison to the user gender ratio.
                    # Divide the colors by the users' gender.
                    # Divide the plots by the auction type.
                    # Divide the line dotting by the advertiser type.
                    # Show the error based on the standard deviation.
                    # Show the data points as dots.
                    sns.relplot(
                        data=advertiser_ratio, x="Female to Male Ratio", y="Ratio of Ads Seen By User",
                        hue="Sex", style="Advertiser Type", col="Auction Type", kind="line", ci='sd', marker='o',
                        palette=colors
                    )
                    # Include the correct configurations.
                    plt.gcf().text(0.9, 0.8,
                                   "Budget: " + str(budget_size) + "\n"
                                   "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                                   "Advertiser Size: " + str(advertiser_size[i]) + "\n"
                                   "Retailer to Economic Opportunity Ratio: " + str(retail_ratio[j] * 100) + "%\n",
                                   fontsize=10, bbox=props)

                    # Save the figure to the graph folder.
                    plt.savefig(
                        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/percentage to user ratio" + str(
                            budget_size) + population_size[i] + "adv_ratio" + str(r) + ".jpg", bbox_inches='tight')
                    plt.close()

                    # Define the properties for the box with the config informations.
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    # Plot the percentage of ads seen by female and male users in comparison to the advertiser type ratio.
                    # Divide the colors by the users' gender.
                    # Divide the plots by the auction type.
                    # Divide the line dotting by the advertiser type.
                    # Show the error based on the standard deviation.
                    # Show the data points as dots.
                    sns.relplot(
                        data=user_ratio, x='Retailer to Economic \n'
                                           'Opportunity Ratio',
                        y="Ratio of Ads Seen By User", hue="Sex", style="Advertiser Type", col="Auction Type", kind="line", ci='sd', marker='o',
                        palette=colors
                    )
                    # Include the correct configurations.
                    plt.gcf().text(0.9, 0.8,
                                   "Budget: " + str(budget_size) + "\n"
                                   "User Size: " + str(user_size[i] * advertiser_size[i]) + "\n"
                                   "Advertiser Size: " + str(advertiser_size[i]) + "\n"
                                   "Female to Male Ratio: " + str(retail_ratio[j] * 100) + "%\n",
                                   fontsize=10, bbox=props)

                    # Save the figure to the graph folder.
                    plt.savefig(
                        "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/Graph/Revenue Plots/percentage to advertiser ratio" + str(
                            budget_size) + population_size[i] + "user_ratio" + str(r) + ".jpg", bbox_inches='tight')
                    plt.close()

                # Adjust the budget size to have a correct naming.
                budget_size *= 100
            i += 1
    return


# Configure the dataframe with all results correct, to use it for the draw percentage reach graph method.
def complete_data_frame():
    # Open the csv.
    with open("C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long.csv", 'r') as data:
        dataframe = pd.read_csv(data, index_col=0)
        # Print statement to see the progress.
        print("inserting")
        # Fill out the empty configuration lines for each row for one seed. --> Easier to process later.
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

        # Save the newly filled file to the folder.
        dataframe.to_csv(
            "C:/Users/User/Desktop/Studium/Informatik/Bachelorarbeit/data_results/CSV/total/Data_long_filled.csv")

# Call the methods in the correct order.
draw_multiple()
# draw_revenue_graph()
# complete_data_frame()
draw_percentage_reach_graph()

