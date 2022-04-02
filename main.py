import simulation as sim
import pickle
import csv

# TODO: DONE!!!!!

# The variable file name (v.f.n.) is of the form VariablesXXXXX.csv
# To change the file just change the variable: no

no = "1"  # no is the number of the config file
# path to the stored config files
path_dir: str = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\Variables"
path = path_dir + no + ".csv"  # complete path


def get_list_parameters(file_name):
    """We read this variables file and keep it in a dictionary of parameters.
    {parameter_name: parameter_value, ...}"""
    global list_parameters
    with open(file_name, mode='r') as infile:
        reader = csv.reader(infile)
        list_parameters = {rows[0]: rows[1] for rows in reader}
    return list_parameters


# get parameters from variable file
list_parameters = get_list_parameters(path)
# initialise simulation for these parameters
simulation = sim.SingleSimulation(list_parameters)
# run the created simulation (with printing intermediate steps)
simulation.get_stats(True)

# save simulation results in .pkl file with the same number in a separate folder
# TODO: Save the correct things into a pkl!
with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Data" + no + '.pkl', 'wb') as output:
    pickle.dump(simulation, output, pickle.HIGHEST_PROTOCOL)
