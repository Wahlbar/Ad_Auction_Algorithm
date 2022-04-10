import csv
import itertools


# This file was used for:
#  1) generating different parameter configurations
#  2) running multiple simulations at once

# 1) ------------------- Generating variable files -------------------
def write_parameters_into_csv(dict_param, no_comb):
    """ Writes a dictionary of parameters to a file indexed by no_comb."""
    with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files\Variables" + str(no_comb) + '.csv',
              'w') as config_log:
        for key in dict_param.keys():
            config_log.write("%s,%s\n" % (key, dict_param[key]))


# The functions below create different parameter configurations .csv files
def generate_csv_files(no_folders=-1, last_file=0):

    def read_base_parameters():
        infile = open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\base_config.csv", mode='r')
        reader = csv.reader(infile)
        list_parameters_base = {rows[0]: rows[1] for rows in reader}

        return list_parameters_base

    list_parameters_base = read_base_parameters()

    dict_changes = {}
    dict_changes["ratio_advertisers"] = [0.1, 0.2, 0.3, 0.4, 0.5,
                                         0.6, 0.7, 0.8, 0.9]
    dict_changes["ratio_sex_users"] = [0.1, 0.2, 0.3, 0.4, 0.5,
                                       0.6, 0.7, 0.8, 0.9]
    dict_changes["budget"] = [0.05, 0.07, 0.09,
                              0.1, 0.3, 0.5]
    dict_changes["ratio_user_advertiser"] = [10, 100, 1000]
    dict_changes["advertiser_size"] = [10, 100, 1000]
    names_basic = list(dict_changes.keys())

    def all_basic(no_comb, list_parameters):
        # itertools.product: combines all inputs with each others!
        for comb in itertools.product(dict_changes["ratio_advertisers"],
                                      dict_changes["ratio_sex_users"],
                                      dict_changes["budget"],
                                      dict_changes["ratio_user_advertiser"],
                                      dict_changes["advertiser_size"]):

            # --1-- change the basic parameters
            for k in range(len(names_basic)):
                list_parameters[names_basic[k]] = comb[k]

            # write a new file
            no_comb += 1
            write_parameters_into_csv(list_parameters, no_comb)

        return no_comb
    all_basic(0, list_parameters_base)
    no_comb = last_file

    # ---change the file_names.txt to have all the above files
    for i in range(no_folders):
        f = open("file_names" + str(i + 1) + ".txt", mode='w')
        for j in range(last_file, no_comb):
            if j % no_folders == i:
                f.writelines(('Variables' + str(j + 1) + '.csv\n'))

    return no_comb


# generate files
generate_csv_files()
