import simulation as sim
import csv
import os

# TODO: DONE!!!!! Only do parameter combinations that answer an interesting answer.

# The variable file name (v.f.n.) is of the form VariablesXXXXX.csv


def run_one_file(number):
    def get_list_parameters(no):
        """We read this variables file and keep it in a dictionary of parameters.
        {parameter_name: parameter_value, ...}"""
        global list_parameters
        with open(
                r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files\Variables" + str(no) + ".csv",
                mode='r') as infile:
            reader = csv.reader(infile)
            list_parameters = {rows[0]: rows[1] for rows in reader}
        return list_parameters

    # get parameters from variable file
    list_parameters = get_list_parameters(number)
    # initialise simulation for these parameters
    simulation = sim.SingleSimulation(list_parameters)
    return simulation.get_stats()


def run_multiple():
    """Runs a simulation for each parameter combination file listed in file_name
    File_name should have multiple lines, each with a "VariablesXXXXX.csv" """
    # folder path
    dir_path = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files"
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1

    # finished simulation until and including 92!
    for i in range(729, 972):
        print("Simulation: ", i+1)
        simulation_1, simulation_2 = run_one_file(i+1)
        with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\Unrestrained GSP\Data" + str(i+1) + ".csv",
                  'w') as output:
            write = csv.writer(output)
            write.writerow(sim.write_header())
            for j in range(len(simulation_1)):
                write.writerow(simulation_1[j])

        with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\CSV\Separated Slots GSP\Data" + str(i+1) + ".csv",
                  'w') as output:
            write = csv.writer(output)
            write.writerow(sim.write_header())
            for j in range(len(simulation_2)):
                write.writerow(simulation_2[j])

# run big simulations only for one set of parameters and then say that there are no significant differences.

run_multiple()
