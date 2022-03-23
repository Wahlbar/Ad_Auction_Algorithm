### Programming Notes:
###

import numpy as np

import Advertiser
import User

userSet = []

nb_male = 0
nb_female = 0
user_size = 1000
# try different numbers: 1000 - 1'000'000, ratio advertiser to user < 1 - 10 %
# make a seed

np.random.seed(14)
for i in range(user_size):
    binary = np.random.randint(0, 2)
    sex = ""
    if binary == 0:
        sex = "f"
        nb_female += 1
    elif binary == 1:
        sex = "m"
        nb_male += 1
    else:
        print("Wrong input for sex: " + sex)
        break
    user = User.User(sex, 0, 0, 0)
    userSet.append(user)

# for user in userSet:
#     print(user)

print("Male: ", nb_male)
print("Female", nb_female)

advertiserSet = []
advertiser_size = 100
advertiser_type_ratio = 0.1
nb_retailer = 0
nb_economic_opportunity = 0
for i in range(advertiser_size):
    binary = np.random.binomial(1, advertiser_type_ratio, 1)
    if binary == 0:
        advertiser_type = "r"
        nb_retailer += 1
    elif binary == 1:
        advertiser_type = "e"
        nb_economic_opportunity += 1
    else:
        print("Wrong input for advertiser type: " + advertiser_type)
        break
    # Draw ad quality from a random number between 0 and 1?
    # Right now I am generating the ad quality from a gaussian
    # distribution -> negative values... should not change much?
    ad_quality = np.random.normal(0, 1, 1)


    # Assign to all advertisers the same ad budget. Later change it depending on the type of advertiser
    ad_budget_universal = 10 ** 10

    # Generate an advertiser
    advertiser = Advertiser.Advertiser(advertiser_type, ad_quality, 0, ad_budget_universal)
    advertiserSet.append(advertiser)

for advertiser in advertiserSet:
    print(advertiser)

print("Retailer: ", nb_retailer)
print("Economic Opportunity: ", nb_economic_opportunity)
