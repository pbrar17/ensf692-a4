# calgary_dogs.py
# Pahul Brar
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

def main():
    import pandas as pd
    import numpy as np

    # Import data here
    data = pd.read_excel("CalgaryDogBreeds.xlsx", header= 0)

    print("ENSF 692 Dogs of Calgary")

    #Making Breed names uppercase, to allow for ease of use and typesafety
    data['Breed'] = data['Breed'].str.upper()

    # User input stage
    # Waiting for user to input a correct breed, raising ValueError until a correct breed entered
    while(True):
        try:
            selection = input("Please enter a dog breed ").strip().upper()
            if(selection not in data['Breed'].values):
                raise ValueError("Dog breed not found in the data. Please try again")
        except ValueError as e:
            print(e)
            continue
        break

    # Data anaylsis stage

    selected_breed_data = data[data['Breed'] == selection]

    top_years_for_breed = selected_breed_data.groupby('Year')['Total'].sum().index.tolist()

    print("The "+ selection + " was found in the top breeds for years:", end=' ')
    
    for y in top_years_for_breed:
        print(y, end = " ")

    #Grouping orignal data by breed and summing it up, so we have overall totals for all breeds
    registration = data.groupby(['Breed'], as_index= False)['Total'].sum()

    #Printing the total overall regesitrations of the breed 
    print()
    print("There have been", end = " ")
    print(registration.loc[(registration['Breed'] == selection), 'Total'].values[0], end = " ")
    print(selection + " dogs registered in total.")

    #Grouping Data by Year and Breed, also summing total up by year for each breed
    annualizedData = data.groupby(['Year', 'Breed'], as_index=False)['Total'].sum()

    # Creating a MultiIndex DataFrame
    multi_index_df = annualizedData.set_index(['Year', 'Breed'])

    # Slicing the DataFrame using IndexSlice
    idx = pd.IndexSlice
    yearData = multi_index_df.loc[:, idx['Total']].groupby('Year').sum()

    selectedSubset = multi_index_df.loc[idx[:, selection], :]

    #Calculating proportion of registration for Selected breed over all breeds, per year
    selectedBreedSum = 0
    allBreedsSum = 0
    
     # Iterating over all of the years
    for year in yearData.index:
        # Initializing counts for the current year to zero
        selectedBreed = 0
        allBreeds = 0

        if (year, selection) in selectedSubset.index:
            # If the selected breed exists for this year, get its count
            selectedBreed = selectedSubset.loc[(year, selection), 'Total']

        # Get the total count for all breeds for this year
        allBreeds = yearData.loc[year]

        selectedBreedSum += selectedBreed
        allBreedsSum += allBreeds

        #Printing the proportion of selction for the year for the chosen breed
        print(f"The {selection} was {((selectedBreed/allBreeds) * 100):.6f}% of top breeds in {year}.")

    #Printing the proportion of selction overall for the chosen breed
    print(f"The {selection} was {((selectedBreedSum/allBreedsSum) * 100):.6f}% of top breeds across all years.")

    #Monthly grouped data for selected breed
    monthData = data.loc[data['Breed'] == selection].groupby("Month").count()

    #Max times a month appears for the breed
    max_total = np.max(monthData['Total'])

    # Mapping the monthData Total to the maximum total for the selected breed
    max_indices = monthData[monthData['Total'] == max_total].index.tolist()

    #Printing most popular months
    print("Most popular month(s) for "+ selection + ":", end=' ')
    for month in max_indices:
        print(month,end = " ")   
    print()



# LABRADOR RETR

if __name__ == '__main__':
    main()
