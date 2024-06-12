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

    data['Breed'] = data['Breed'].str.upper()

    # User input stage
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

    annualizedData = data.groupby(['Year', 'Breed'], as_index=False)['Total'].sum()

    top_breed = set()
    for year in annualizedData['Year'].values:
        thisYear = annualizedData[annualizedData['Year'] == year]
        max = np.max(thisYear['Total'])

        totalForSelection =  annualizedData.loc[(annualizedData['Breed'] == selection) & (annualizedData['Year'] == year), 'Total'].values[0]
        if(max == totalForSelection):
            top_breed.add(year)
    
    top_breed = np.sort(list(top_breed))
    print("The "+ selection + " was found in the top breeds for years:", end=' ')
    for y in top_breed:
        print(y, end = " ")

    registration = data.groupby(['Breed'], as_index= False)['Total'].sum()

    print()
    print("There have been", end = " ")
    print(registration.loc[(registration['Breed'] == selection), 'Total'].values[0], end = " ")
    print(selection + " dogs registered in total.")

    # Creating a MultiIndex DataFrame
    multi_index_df = annualizedData.set_index(['Year', 'Breed'])

    # Slicing the DataFrame using IndexSlice
    idx = pd.IndexSlice
    yearData = multi_index_df.loc[:, idx['Total']].groupby('Year').sum()

    selectedSubset = multi_index_df.loc[idx[:, selection], :]

    selectedBreedSum = 0
    allBreedsSum = 0

    for year in yearData.index:
        selectedBreed = selectedSubset.loc[idx[year, selection], 'Total']
        allBreeds = yearData.loc[year]

        selectedBreedSum += selectedBreed
        allBreedsSum += allBreeds

        print(f"The {selection} was {((selectedBreed/allBreeds) * 100):.6f}% of top breeds in {year}.")



    print(f"The {selection} was {((selectedBreedSum/allBreedsSum) * 100):.6f}% of top breeds across all years.")

    monthData = data.loc[data['Breed'] == selection].groupby("Month").count()

    max_total = monthData['Total'].max()

    # Mapping the monthData Total to the maximum total for the selected breed
    max_indices = monthData[monthData['Total'] == max_total].index.tolist()



    print("Most popular month(s) for "+ selection + ":", end=' ')
    for month in max_indices:
        print(month,end = " ")   
    print()



# LABRADOR RETR

if __name__ == '__main__':
    main()
