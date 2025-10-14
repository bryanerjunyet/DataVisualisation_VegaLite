import pandas as pd
import os

def main():
    # Read the crime data
    crime_df = pd.read_csv('full_visualisation/data/multiline_data/crime_district_cleaned.csv')
    
    # Read the population data
    population_df = pd.read_csv('full_visualisation/data/multiline_data/population_state.csv')
    
    # Debug: Print column names to understand the structure
    print("Crime data columns:", crime_df.columns.tolist())
    print("Population data columns:", population_df.columns.tolist())
    print("Sample population data:")
    print(population_df.head())
    
    # Filter population data for sex=both, age=overall, ethnicity=overall
    filtered_pop = population_df[
        (population_df['sex'] == 'both') & 
        (population_df['age'] == 'overall') & 
        (population_df['ethnicity'] == 'overall')
    ]
    
    # Extract year from date column and calculate total population for Malaysia by year
    # Assuming date is in YYYY-MM-DD format, extract the year
    filtered_pop['year'] = pd.to_datetime(filtered_pop['date']).dt.year
    malaysia_population = filtered_pop.groupby('year')['population'].sum() * 1000
    
    print("Malaysia population by year:")
    print(malaysia_population)
    
    # Check crime data column names (assuming they might be 'category' and 'type' instead)
    # Filter crime data for Assault and Property crime types
    if 'Crime_Type' in crime_df.columns:
        assault_property_crimes = crime_df[crime_df['Crime_Type'].isin(['Assault', 'Property'])]
        total_cases_by_year = assault_property_crimes.groupby('Year')['Cases'].sum()
    elif 'category' in crime_df.columns:
        assault_property_crimes = crime_df[crime_df['category'].isin(['assault', 'property'])]
        total_cases_by_year = assault_property_crimes.groupby('date')['crimes'].sum()
        # If date is in YYYY-MM-DD format, extract year
        total_cases_by_year.index = pd.to_datetime(total_cases_by_year.index).year
    else:
        print("Error: Could not find appropriate crime type column")
        return
    
    print("Total cases by year:")
    print(total_cases_by_year)
    
    # Create result dataframe
    result_df = pd.DataFrame({
        'Year': total_cases_by_year.index,
        'Total_Cases': total_cases_by_year.values
    })
    
    # Merge with population data and calculate crimes per 10k population
    result_df['Population'] = result_df['Year'].map(malaysia_population)
    result_df['crimes_per_10k_population'] = (result_df['Total_Cases'] / result_df['Population']) * 10000
    
    print("Population mapping:")
    print(result_df[['Year', 'Population']].head())
    
    # Select final columns
    final_df = result_df[['Year', 'Total_Cases', 'crimes_per_10k_population']]
    
    # Save to CSV
    output_path = 'crime_district_ano_cleaned.csv'
    final_df.to_csv(output_path, index=False)
    
    print(f"Data cleaned and saved to {output_path}")
    print(f"Shape: {final_df.shape}")
    print("\nFirst few rows:")
    print(final_df.head())

if __name__ == "__main__":
    main()