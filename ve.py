import simulation as sim
import csv
import pickle
import itertools
import ast
from os import path
import json
import numpy as np
import matplotlib.pyplot as plt

# Code from Stefania Ionescu

# This file was used for:
#  1) generating different parameter configurations
#  2) running multiple simulations at once

# 1) ------------------- Generating variable files -------------------
def write_parameters(dict_param, no_comb):
    ''' Writes a dictionary of parameters to a file indexed by no_comb.
    '''
    with open('Variables' + str(no_comb) + '.csv', 'w') as f:
        for key in dict_param.keys():
            f.write("%s,%s\n" % (key, dict_param[key]))

# The functions below create different parameter configurations .csv files
def generate_csv_files(file_name, no_folders=-1, last_file=0):
    '''Similarly as above, generates multiple variables csv files'''

    def read_base_parameters(list_parameters_base={}):
        infile = open(file_name, mode='r')
        reader = csv.reader(infile)
        list_parameters_base = {rows[0]: rows[1] for rows in reader}
        # list_parameters_base["orientation_types"] = '"[0, 1]"'
        # list_parameters_base["prob_types"] = '"[0.5, 0.5]"'

        return list_parameters_base

    list_parameters_base = read_base_parameters()

    dict_changes = {}
    dict_changes["random_seed"] = [98188, 66162, 13363, 13235, 36248,
                                   22699, 73828, 8560, 26797, 78100]
    # dict_changes["filter"] = ["OFF", "WEAK", "STRONG", "non_bias_WEAK", "non_bias_STRONG"]
    # dict_changes["norm_intervention"] = ["0", "1"]
    names_basic = list(dict_changes.keys())

    def all_basic(no_comb, list_parameters):
        # itertools.product: combines all inputs with each others!
        # TODO: Change the dict_changes to my variables!
        for comb in itertools.product(dict_changes["random_seed"],
                                      dict_changes["filter"],
                                      dict_changes["norm_intervention"]):
            # --1-- change the basic parameters
            for k in range(len(names_basic)):
                list_parameters[names_basic[k]] = comb[k]

            # write a new file
            no_comb += 1
            write_parameters(list_parameters, no_comb)

        return no_comb

    no_comb = last_file
    # TODO: Change to own correlation. Here: beta = correlation level between the bias and non-bias attributes, gamma = correlation level between the value of matching and competing attributes
    attr_params = ['beta', 'gamma']
    combs = [['0.8', '0.6'], ['0', '0.6'], ['0.4', '0.6'], ['0.6', '0.6']]
    for c in combs:
        for i in range(2):
            list_parameters_base[attr_params[i]] = c[i]
        no_comb = all_basic(no_comb, list_parameters_base)

    list_parameters_base = read_base_parameters()

    attr_params = ['no_matching_searchable', 'no_matching_experiential',
                   'no_competing_searchable', 'no_competing_experiential']
    combs = [['1', '1', '1', '2'], ['1', '1', '2', '1'], ['1', '2', '1', '1'], ['2', '1', '1', '1']]
    combs += [['1', '1', '2', '2'], ['1', '2', '2', '1'], ['2', '2', '1', '1'],
              ['2', '1', '1', '2'], ['2', '1', '2', '1'], ['1', '2', '1', '2']]
    for c in combs:
        for i in range(4):
            list_parameters_base[attr_params[i]] = c[i]
        no_comb = all_basic(no_comb, list_parameters_base)

    # ---change the file_names.txt to have all the above files
    for i in range(no_folders):
        f = open("file_names" + str(i+1) + ".txt", mode='w')
        for j in range(last_file, no_comb):
            if j % no_folders == i:
                f.writelines(('Variables' + str(j+1) + '.csv\n'))

    return no_comb

# 2) ------------ For running the experiment -------------------
def run_one(file_name):
    '''Does multiple experiments for different sets of parameters.
    file name needs to be "VariablesXXXXX.csv"
    This is similar with run_one.py
    '''

    def get_list_parameters(file_name):
        '''We read this variables file and keep it in a dictionary.
        e.g. file_name = Variables.csv '''
        global list_parameters
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            list_parameters = {rows[0]: rows[1] for rows in reader}

        return list_parameters

    list_parameters = get_list_parameters(file_name)

    # TODO: Find out why starting from 9 to -4 and adjust it to my model!
    no = file_name[9:]
    no = no[:-4]

    # TODO: Use it for your simulation! Import SingleSimulation
    # perform the simulation (and also change the name of the current file)
    s = sim.SingleSimulation(list_parameters)
    s.get_stats()

    # save simulation results
    with open('Stats' + no + '.pkl', 'wb') as output:
        pickle.dump(s, output, pickle.HIGHEST_PROTOCOL)

# TODO: This is perfect. Copy it!
def run_multiple(file_name):
    '''Runs a simulation for each parmaeter combination file listed in file_name
    File_name should have multiple lines, each with a "VariablesXXXXX.csv" '''

    file_names = open(file_name, mode='r').readlines()
    for file_name in file_names:
        file_name = file_name.rstrip("\n\r")
        print(file_name)
        run_one(file_name)


def read_stats(file_name):
    ''' reads a .pkl file.'''
    with open(file_name, 'rb') as input:
        s = pickle.load(input)
        return s

# TODO: Maybe useful
def make_simulations(list_stats_no, criteria='NONE', stats_no_param={}):
    ''' Makes an object of type Simulations with all the statistics
       between in the list.
       criteria = dictionary of setted parameter values'''

    # TODO: Not sure if I need this!
    def match_criteria(dict_param, criteria):
        ''' Checks if a dict of parameters matches a given list of criteria'''
        match = True
        for c_name in criteria.keys():
            if str(dict_param[c_name]) not in ast.literal_eval(criteria[c_name]):
                match = False
        return match

    sims = []
    for no in list_stats_no:
        file_name = 'Stats' + str(no) + '.pkl'
        if path.exists(file_name):
            with open(file_name, 'rb') as input:
                if criteria == 'NONE':
                    s = pickle.load(input)
                    sims.append(s)
                elif match_criteria(stats_no_param[no], criteria):
                    s = pickle.load(input)
                    sims.append(s)
    return sim.Simulations(sims)

# TODO: Maybe useful
def changing_file(no_stats, start=1):
    '''Makes a .csv file with the changing parameters.
    Returns a dictionary {no_stats: {dict_parameters}}'''

    list_stats_no = range(start, start + no_stats)
    sims = make_simulations(list_stats_no)

    def write_parameters(dict_param):
        with open('Changing.csv', 'w') as f:
            f.write("Variable name, Options, Choice for plotting\n")
            for key in dict_param.keys():
                f.write('%s,"%s"\n' % (key, dict_param[key]))
    write_parameters(sims.identify_changing_parameters())

    # make the dictionary of statistics parameters
    stats_no_param = {}
    for no in list_stats_no:
        file_name = 'Stats' + str(no) + '.pkl'
        if path.exists(file_name):
            with open(file_name, 'rb') as input:
                s = pickle.load(input)
                stats_no_param[no] = s.parameters
    return stats_no_param

# TODO: Useful adjust plotting
def plot(no_stats, start=1, hand_filter=False, file_name='NONE', stats_no_param={}):
    ''' Loads, filters, and plots statistics.
    no_stats = either no of statistics or file name with choices'''

    list_stats_no = range(start, start + no_stats)
    if hand_filter:
        sims = make_simulations(list_stats_no)
        sims.filter_multiple()
    else:
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            list_criteria = {rows[0]: rows[2] for rows in reader}
            list_criteria.pop('Variable name')
        sims = make_simulations(list_stats_no, list_criteria, stats_no_param)

    return sims
    # TODO: Look into these functions
    sims.remove_duplicates()
    sims.group_by_non_seed()
    sims.plot_stats(True)

    return sims


'''
To plot statistics from cluster run with parameter choice from file,
do the following steps:
1. stats_no_param = ve.changing_file(237)
generate a .csv file with the changing parameters
  + a mapping form the files to the parameters
2. modify it to have the values you want to plot
3. ve.plot(499000, file_name = "Changing.csv", stats_no_param=stats_no_param)
'''
# TODO: Stopped here

def make_json(list_stats_no):
    '''Given a list of simulations, makes a csv file with parameters and
    statistics'''

    sims_dict = {}
    for no in list_stats_no:
        file_name = 'Stats' + str(no) + '.pkl'
        if(no % 1000 == 0):
            print(no)
        if path.exists(file_name):
            # TODO: Change the names, such that it matches my naming!
            with open(file_name, 'rb') as input:
                s = pickle.load(input)
                sims_dict[no] = {}
                sims_dict[no]['parameters'] = s.parameters
                sims_dict[no]['statistics'] = {}
                sims_dict[no]['statistics']['no_long_term'] = list(s.statistics.no_long_term)
                sims_dict[no]['statistics']['no_first_date'] = list(s.statistics.no_first_date)
                sims_dict[no]['statistics']['no_second_date'] = list(s.statistics.no_second_date)
                sims_dict[no]['statistics']['no_outgroup_long_term'] = list(
                    s.statistics.no_outgroup_long_term)
                sims_dict[no]['statistics']['percentage_outgroup_long_term'] = list(
                    s.statistics.percentage_outgroup_long_term)
                sims_dict[no]['statistics']['no_online'] = list(s.statistics.no_online)
                sims_dict[no]['statistics']['no_outgroup_online'] = list(
                    s.statistics.no_outgroup_online)
                sims_dict[no]['statistics']['no_offline'] = list(s.statistics.no_offline)
                sims_dict[no]['statistics']['no_outgroup_offline'] = list(
                    s.statistics.no_outgroup_offline)

    with open('simulations.json', 'w') as f:
        json.dump(sims_dict, f)


def make_csv(sims='no', no='no'):
    ''' Makes a csv file that only keeps:
    - the relevant parameters (i.e. the ones that are changing)
    - the last value of the percentage of long-term out-group rel
    It creates the csv either from a simulaiton object, or
       from .pkl files indexed from 1 to no.
    '''
    import csv

    if no != 'no':
        stats_no_param = changing_file(no)
        print('go and change the file Change.csv')
        input()
        sims = plot(no, file_name="Changing.csv", stats_no_param=stats_no_param)

    changing_params = sims.identify_changing_parameters()
    names_changing_params = list(changing_params.keys())
    sims.remove_duplicates(True)

    list_dict = []
    for s in sims.list_simulations:
        d = {}
        for p in names_changing_params:
            d[p] = s.parameters[p]

        d['percentage_outgroup_long_term'] = s.statistics.percentage_outgroup_long_term[-1]
        d['no_first_date'] = s.statistics.no_first_date['total']
        d['no_second_date'] = s.statistics.no_second_date['total']
        d['no_long_term'] = s.statistics.no_long_term[-1]
        d['no_outgroup_long_term'] = s.statistics.no_outgroup_long_term[-1]

        d['exit_reason_bad_rec'] = s.statistics.exit_reason["Too many bad recommendations"]
        d['exit_reason_failed_rel'] = s.statistics.exit_reason['Too many failed relationships']
        d['exit_reason_long_term'] = s.statistics.exit_reason["Long term relationship"]

        d['time_searching'] = s.statistics.percentage_of_time_by_phase['searching']
        d['time_offline'] = s.statistics.percentage_of_time_by_phase['offline_rel']

        d['no_oglt_low'] = s.statistics.no_outgroup_long_term_by_type['low']
        d['no_oglt_med'] = s.statistics.no_outgroup_long_term_by_type['medium']
        d['no_oglt_high'] = s.statistics.no_outgroup_long_term_by_type['high']
        '''
        self.exit_reason = {"Too many bad recommendations": 0,
                            "Too many failed relationships": 0, "Long term relationship": 0}
        # where did agents mostly spend their time
        self.time_by_phase = {"searching": 0, "online_rel": 0, "offline_rel": 0}
        self.percentage_of_time_by_phase = {"searching": 0, "online_rel": 0, "offline_rel": 0}
        # why do users form long-term rel
        self.no_outgroup_long_term_by_type = {'low': 0, 'medium': 0, 'high': 0}'''
        names_fields = list(d.keys())
        list_dict.append(d)

    with open('simulations.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=names_fields)
        writer.writeheader()
        for data in list_dict:
            writer.writerow(data)

    import pandas as pd
    return pd.read_csv('simulations.csv')


def plot_hit_new(df):
    '''Makes plot with error bars for a given dataframe of results'''
    import seaborn as sns
    import pandas as pd

    #df = pd.read_csv(file_name)
    has_2_attr = abs(df['no_matching_searchable']-0)+abs(df['no_competing_searchable']-1) == 0
    df_2 = df[has_2_attr]
    fig = sns.catplot(x="filter", y="percentage_outgroup_long_term",
                      hue="norm_intervention", kind="bar", data=df_2,
                      legend_out=False)

    fig.set(xlabel='Filter intervention', ylabel='Percentage of out-group long-term relationships')

    # change y axis to percentage
    from matplotlib.ticker import PercentFormatter
    for ax in fig.axes.flat:
        ax.yaxis.set_major_formatter(PercentFormatter(1))

    # change legend
    # title
    new_title = 'Norm intervention'
    fig._legend.set_title(new_title)
    # replace labels
    new_labels = ['On', 'Off']
    for t, l in zip(fig._legend.texts, new_labels):
        t.set_text(l)

    #plt.legend(loc='best', title='Norm intervention')

    plt.show()


def make_hist_dict(sims, criterias):
    '''Make the dictionaries for plotting histograms.
    Need to have with and without intervention, and the 3 filtering options.
    Can modify the groupping function
    criterias = {name: {criteria}}'''

    no_criterias = len(criterias.keys())

    def match_criteria(dict_param, criteria):
        ''' Checks if a dict of parameters matches a given list of criteria
        criteria = dictionary of setted parameter values'''
        match = True
        for c_name in criteria.keys():
            if str(dict_param[c_name]) not in criteria[c_name]:
                match = False
        return match

    d_without = {}
    d_with = {}
    filter = ["OFF", "WEAK", "STRONG"]
    for f in filter:
        d_without[f] = list(np.zeros(no_criterias))
        d_with[f] = list(np.zeros(no_criterias))

    for s in sims.list_simulations:
        par = s.parameters
        for i in range(no_criterias):
            c_name = list(criterias.keys())[i]
            if match_criteria(par, criterias[c_name]):
                if par['norm_intervention'] == '0':
                    for f in filter:
                        if par['filter'] == f:
                            d_without[f][i] = s.statistics.percentage_outgroup_long_term[-1]
                else:
                    for f in filter:
                        if par['filter'] == f:
                            d_with[f][i] = s.statistics.percentage_outgroup_long_term[-1]
    return (d_without, d_with, list(criterias.keys()))


def plot_histogram(dictionary_results_without, dictionary_results_with, x_labels):
    '''
    Plots the statistics with the number of articles in the past month.
    dictionary_results = dictionary of the form query_term: [no_articles_for_period_1, no_articles_for_period_2, ...]
        dict_results2 = {'OFF': [0.056606879431433034], 'WEAK': [0.0866547843922199], 'STRONG': [0.039150828082210466]}
        plot_no_articles(dict_results2, ['2'])
    '''

    d0 = dictionary_results_with
    d1 = dictionary_results_without
    labels = x_labels
    query_terms = list(d0.keys())
    list_0 = d0[query_terms[0]]
    list_1 = d0[query_terms[1]]
    list_2 = d0[query_terms[2]]
    list_0_1 = d1[query_terms[0]]
    list_1_1 = d1[query_terms[1]]
    list_2_1 = d1[query_terms[2]]

    x = np.arange(0, len(labels))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots(figsize=(18, 5))
    rects1 = ax.bar(x - width, list_0, width-0.01, label='Norm intervention', color='r', alpha=0.7)
    rects2 = ax.bar(x, list_1, width-0.01, color='r', alpha=0.7)
    rects3 = ax.bar(x + width, list_2, width-0.01, color='r', alpha=0.7)
    rects1_1 = ax.bar(x - width, list_0_1, width-0.01, label=query_terms[0])
    rects2_1 = ax.bar(x, list_1_1, width-0.01, label=query_terms[1])
    rects3_1 = ax.bar(x + width, list_2_1, width-0.01, label=query_terms[2])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Number of non-bias attributes')
    ax.set_ylabel('Percentage of long-term out-group relationships')
    ax.set_title('Percentage of long-term out-group relationships depending on the intervention')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.autoscale()
    xmin = -2*width
    xmax = max(np.arange(len(labels)))+2*width
    ymin = 0
    ymax = max(list_0+list_1+list_2)*1.1
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax.legend(loc='best')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    '''
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects1_1)
    autolabel(rects2_1)
    autolabel(rects3_1)'''

    # fig.autofmt_xdate()

    fig.tight_layout()

    plt.show()


def check_stats(sim):
    st = sim.statistics

    # dorp after first date
    fd = st.no_first_date
    sd = st.no_second_date
    print('Drop after first date:')
    drop = sd['total'] / fd['total']
    print('   rate ',  drop, ': from ', fd['total'], ' to ', sd['total'])
    out_group_drop = sd['out-group'] / fd['out-group']
    print('   out-group rate ',  out_group_drop, ': from ',
          fd['out-group'], ' to ', sd['out-group'])

    # percentage out-group
    no_lt = st.no_long_term[-1]
    no_oglt = st.no_outgroup_long_term[-1]
    print('\nPercentage out-group long-term: ', no_oglt/no_lt, no_oglt, no_lt)

    # exit-reason, time by state, who in olt
    print('\nExit reason\n', st.exit_reason)
    print('\nTime by phase\n', st.percentage_of_time_by_phase)
    print('\nOut-group long-term by type\n', st.no_outgroup_long_term_by_type)