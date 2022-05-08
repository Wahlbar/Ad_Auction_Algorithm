# Online Ad Auction Simulation
### An agent-based model to simulate online generalized-second prize ad auctions to examine discrimination caused by competition overflow.

This repository contains an agent-based simulation for an unrestrained, and a separated slots GSP online ad auction. 
It simulates a set of advertisers bidding on a set of users to display their advertisements.

For detailed information refer to my bachelor thesis: "Fairness in Online Ad Auctions: the Role of the Auction Mechanism".

The main structure for using this simulation is as follows:

A. Generating the configuration files: 
1. Save the example_base_configuration.csv in you preferred folder or create your own .csv file with the same structure.
2. Change the path opening the .csv inside the csv_generator.py to the location of your .csv file
3. Change the path saving the .csv configuration files to your preferred location.
4. Run the csv_generator.py to create the different configuration files for the simulations with different parameters.

B. Running the simulation:
5. Change the folder path for opening the configuration inside the main.py to the location defined in 3.
6. Change the folder paths for saving the output statistics to your preferred folders. (I for example saved the output for the unrestrained, and the separated slots auctions in different folders.)
7. Run the main.py file to run all simulations inside the specified folder. To only run one file set the index before the for-loop to the preferred file number. (For large user and advertiser sizes reduce the number of seeds inside the simulation.py, otherwise the simulation can be quite long.)

C. Plotting the results:
8. Change the folder paths for opening the output statistics in the graph.py to the paths specified in 6.
9. Change the folder paths for saving the plots to the preferred folder locations. (I made three folders. One for each auction and one for combined plots.)
10. Run the graph.py and evaluate the graphs. (For rerunning the file, you can sometimes comment some functions out, to reduce the computation time.)

## Programming language
The simulation is coded in Python - version 3.8.8.

## Files
Before running the code, please make sure all the required libraries are installed. For each *.py file, the used libraries are imported at the top of the code.

In this repository, you will find the following files:

### example_base_config.csv
An example file with all the configuration parameters. 
This file shows the layout for the config files, which are generated in the csv_generator.py class. 
However, I implemented the combinations of the different variables static inside the csv_generator.py class.
To change these variables, look inside the csv_generator.py class.

To get the code running, change the folder paths inside the csv_generator.py, main.py and graph.py classes to your own preferred folder path.

Note that the constant variables from the example_base_config_file.csv are used to generate the csv.
When using an own .csv file, try to keep the structure of this file. (Only the first two rows are relevant.)

### csv_generator.py

This class generates all possible combinations of the variable configuration parameters as .csv:

1. ratio_user_advertiser: [100, 10] (size of the users in comparison to the advertiser size)
2. advertiser_size: [100, 10] (site of the advertisers)
3. ratio_advertisers: [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] (ratio of retail advertisers to economic opportunity advertisers)
4. ratio_sex_users: [0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9] (ratio of female to male users) 
5. budget: [100, 1000, 10000] (advertisers budget)
6. All other constant variables shown in the example_base_config.csv

It saves them in the defined folder path.
The advertiser and user sizes are at a mediocre level to reduce the computation time.

### main.py

This class goes through all the generated .csv files and runs an unrestrained, and a separated slots auction.
It tracks the output statistics and saves them for each auction into a different .csv output file.
To only run one simulation fix the index variable after counting the .csv files.

### simulation.py

This class is responsible for running one simulation with different random seeds. (It is used in the main.py)
It tracks the output statistics and passes them to the main.py.
To reduce the computation time for large sample sizes, reduce the random_seed list in this class.

### unrestrained_auction.py & separated_slots_auction.py

These two classes are responsible for the different auctions. 
The main difference between them is that the separated slots auction randomly assigns to each ad slot of a user an advertiser type.
Only advertisers of the assigned type can bid on the specific slot.

Both classes iterate through the users and let each advertiser estimate their expected values on the user.
Afterwards the advertisers with the top x expected values win the auction, where x is the amount of user slots.
They then adjust their bid according to the balanced bidding model.
Then the advertiser pay, and the statistics update (user/advertiser type, platform revenue, etc.).

### user.py

This class defines the user and their attribute.
Right now the only attribute taken into consideration is a binary gender (female, male).
However, further attributes are implemented but not used. 
In future updates (if happening), I will try to generate more detailed users with non-binary attributes.

### advertiser.py

This class defines the advertiser and their attributes.
Right now the advertiser only vary in their type: retail or economic opportunity.
The advertiser's type defines from which distribution they are drawing the user's expected value per click.
Retailers prefer female to male users, while economic opportunity advertisers don't differentiate between male and female users.

### population.py

This class is unused at the moment. Its purpose would be to draw the user's age from a real world population.
Here swiss adult population between 18 and 65.

### graph.py

This class reads the output statistics and plots them. 
It plots the absolute and relative number of retail and economic opportunity ads shown to female and male users for the different auction types.
Next, it plots the platform revenue in dependence of changing user and advertiser size. 
Finally, it also plots the relative number of retail and economic opportunity ads shown to female and male user for the different auctions and varying user and advertiser ratios. 
Adjust the folder path accordingly!