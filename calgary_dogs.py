# calgary_dogs.py
# AUTHOR NAME: Rana Elsadig
# A terminal-based application for computing and printing statistics based on given input.

import numpy as np
import pandas as pd
from collections import Counter

def main():
    """
    Main function to compute and print statistic on the most popular licensed dog breeds in the city of Calgary.

    Prompts the user for a dog breed then prints registration statistics for that breed.

    Returns:
        None
    """

    # Import data here
    all_data = pd.read_excel(r"CalgaryDogBreeds.xlsx")

    # Set indices
    all_data.set_index(['Breed', 'Year', 'Month'], inplace = True)

    print("ENSF 692 Dogs of Calgary")
    # User input stage
    while(True):
        try:
            # Prompt user for a dog breed
            user_input = str(input("Please enter a dog breed: ")).upper()

            # Check if the user's input is a valid school breed, if not, raise a ValueError
            if (user_input not in all_data.index.levels[0]):
                raise ValueError
        except ValueError:
            # Print error if dog breed is not in data, and prompt again
            print("Dog breed not found in the data. Please try again.")
        else:
            # Data anaylsis stage
            # Use masking operation to filter out data dog breed from users input, and print the years where breed is listed in the top.
            breed_mask = all_data.index.get_level_values('Breed') == user_input
            all_breed_data = all_data[breed_mask]
            years_listed = all_breed_data.index.get_level_values('Year').unique()
            print(f"The {user_input} was found in the top breeds for years: ", end="")
            for year in years_listed:
                print(year, end=" ")
            print(" ")
            
            # Sum the total registrations for the dog breed across all years
            registrations_total =  all_breed_data['Total'].sum()
            print(f"There have been {registrations_total} {user_input} dogs registered total")

            # List of years
            years = [2021, 2022, 2023]

            # Initialize total registratiosn for analyzed breed, to be kept count of when computing percentage of breed registrations
            total_breed_registrations = 0

            # Initialize index slice object
            idx = pd.IndexSlice

            for year in years:
                # Use index slice to sum up the total registrations for each year across all breeds
                year_filter = idx[:, year, :]
                year_data = all_data.loc[year_filter]
                year_total = year_data['Total'].sum()

                # Use index slice to sum the total registrations for each year for the inputted breed
                breed_filter = idx[user_input, year, :]
                breed_data = all_data.loc[breed_filter]
                breed_total = breed_data['Total'].sum()
                total_breed_registrations += breed_total

                # Calculate and print the percentage of selected breed registrations out of the total percentage for each year
                registration_year_percentage = (breed_total / year_total) * 100
                print(f"The {user_input} was {registration_year_percentage:.6f}% of top breeds in {year}.")

            # Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
            total_registrations = all_data.groupby('Year').sum()['Total'].sum()
            registration_percentage = (total_breed_registrations / total_registrations) * 100
            print(f"The {user_input} was {registration_percentage:.6f}% of top breeds across all years.")
            
            # Create a set of registration months for the selected breed for each year
            month_sets = [list(all_data.loc[idx[user_input, year, :]].index.get_level_values('Month')) for year in years]
            flattened_month_list = [item for subset in month_sets for item in subset]
            counts = Counter(flattened_month_list)
            if counts:
                # Use counter to determine the months where the registrations were the most popular for the selected breed
                max_count = max(counts.values())
                most_common_values = [key for key, value in counts.items() if value == max_count]

            # Print the most popular months
            print(f"Most popular month(s) for {user_input} dogs: ", end = "")
            for value in most_common_values:
                print(value, end=" ")
            print("")
            break
  

if __name__ == '__main__':
    main()
