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
    print("Variables" + str(number))
# initialise simulation for these parameters
    simulation = sim.SingleSimulation(list_parameters)
    simulation.get_stats()

    with open(r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\data_results\Data" + str(number) + '.csv',
              'w') as output:
        write = csv.writer(output)
        write.writerows(simulation.output)
        for key, value in list_parameters.items():
            write.writerow([key, value])


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

    for i in range(count):
        run_one_file(i+1)


run_one_file(10000)

#run_multiple()
