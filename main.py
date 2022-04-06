import simulation as sim
import pickle
import csv

# TODO: DONE!!!!! Only do parameter combinations that answer an interesting answer.

# The variable file name (v.f.n.) is of the form VariablesXXXXX.csv
# To change the file just change the variable: no

number = "1"  # no is the number of the config file


def get_list_parameters(no):
    """We read this variables file and keep it in a dictionary of parameters.
    {parameter_name: parameter_value, ...}"""
    global list_parameters
    with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\Variables" + no + ".csv", mode='r') as infile:
        reader = csv.reader(infile)
        list_parameters = {rows[0]: rows[1] for rows in reader}
    return list_parameters


# get parameters from variable file
list_parameters = get_list_parameters(number)
# initialise simulation for these parameters
simulation = sim.SingleSimulation(list_parameters)
# run the created simulation (with printing intermediate steps)
simulation.get_stats(True)

# save simulation results in .pkl file with the same number in a separate folder
# TODO: Save solutions in csv or json!
with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Data" + number + '.csv', 'w') as output:
    write = csv.writer(output)
    write.writerows(simulation.output)
    for key, value in list_parameters.items():
        write.writerow([key, value])


