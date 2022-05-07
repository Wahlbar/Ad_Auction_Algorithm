import csv
import itertools

'''
This class generates all possible combinations of configuration parameters from an initial config file as csv files.
'''


# This method saves the parameters into a csv file.
def write_parameters_into_csv(dict_param, no_comb):
    with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files\Variables" + str(
            no_comb) + '.csv',
              'w') as config_log:
        for key in dict_param.keys():
            config_log.write("%s,%s\n" % (key, dict_param[key]))


# This method reads the base_config file and generates all possible combination from the following parameters:
def generate_csv_files(no_folders=-1, last_file=0):

    # Read the base config file and save the parameters in a dictionary.
    def read_base_parameters():
        infile = open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\base_config.csv", mode='r')
        reader = csv.reader(infile)
        list_base = {rows[0]: rows[1] for rows in reader}

        return list_base

    # Save the base parameters.
    list_parameters_base = read_base_parameters()

    # Generate a dictionary of the parameters which can vary and use it to generate any combination of them.
    # TODO: Make this more dynamic (dependent from the config_csv), instead of static. Maybe use numbers for the first x rows.
    dict_changes = {"ratio_user_advertiser": [100, 10],
                    "advertiser_size": [100, 10],
                    "ratio_advertisers": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
                    "ratio_sex_users": [0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9],
                    "budget": [100, 1000, 10000]}

    # Save the keys to later correctly save the parameter names.
    names_basic = list(dict_changes.keys())

    # Combines all inputs with each others.
    def all_basic(no_comb, list_parameters):
        # For each combination:
        for comb in itertools.product(dict_changes["ratio_user_advertiser"],
                                      dict_changes["advertiser_size"],
                                      dict_changes["ratio_advertisers"],
                                      dict_changes["ratio_sex_users"],
                                      dict_changes["budget"]):

            # 1. Save the combined parameters.
            for k in range(len(names_basic)):
                list_parameters[names_basic[k]] = comb[k]

            # 2. Save the whole configuration into a new csv.
            no_comb += 1
            write_parameters_into_csv(list_parameters, no_comb)

        return no_comb

    # Call the function all_basic
    all_basic(0, list_parameters_base)
    no_comb = last_file

    # Rename the files to Variables + number.
    for i in range(no_folders):
        f = open("file_names" + str(i + 1) + ".txt", mode='w')
        for j in range(last_file, no_comb):
            if j % no_folders == i:
                f.writelines(('Variables' + str(j + 1) + '.csv\n'))

    return no_comb


# Generate files.
generate_csv_files()
