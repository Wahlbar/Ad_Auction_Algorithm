import simulation as sim
import csv
import os

'''
This class opens up the config csv files and runs an auction with its parameters
'''


# This method runs one file, given the csv number.
def run_one_file(number):
    # Open the file and save the configuration parameters into a dictionary.
    def get_list_parameters(no):
        global list_parameters
        with open(
                r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files\Variables" + str(no) + ".csv",
                mode='r') as infile:
            reader = csv.reader(infile)
            list_parameters = {rows[0]: rows[1] for rows in reader}
        return list_parameters

    # Get the parameters from variable file.
    list_parameters = get_list_parameters(number)
    # Initialise simulation for these parameters.
    simulation = sim.SingleSimulation(list_parameters)
    return simulation.get_stats()


# This method counts all csv files inside the config_files folder and runs for each one a simulation.
def run_multiple():
    # Folder path.
    dir_path = r"C:\Users\User\Desktop\Studium\Informatik\Bachelorarbeit\config_files\generated_files"
    count = 0
    # Iterate directory.
    for path in os.listdir(dir_path):
        # Check if current path is a file.
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1

    # For each file make an unrestrained and a separated slot auction and save the outputs into different folders.
    # Maybe partition the simulations as below, since the duration is very long otherwise.
    for i in range(count):
        print("Simulation: ", i+1)
        # Make both simulations (separated slots and unrestrained).
        simulation_1, simulation_2 = run_one_file(i+1)
        # Save the simulations separately.
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


# Run the simulation step by step.
# 1 - 243: config files with the biggest sample sizes --> slowest. (100 advertiser & 10000 users): seed size: 5
# 243 - 486: 100 advertisers & 1000 users: seed size 10
# 486 - 729: 10 advertisers & 1000 users: seed size: 20
# 729 - 972: 10 advertisers & 100 users: seed size: 25
run_multiple()
