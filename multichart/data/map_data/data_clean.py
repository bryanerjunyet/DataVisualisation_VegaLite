import pandas as pd
from datetime import datetime

def clean_crime_data():
    """
    Clean the crime_district.csv data according to specified requirements:
    1. Remove rows with state = Malaysia
    2. Remove rows with district != All
    3. Remove rows with type != all
    4. Process data for all years (2016-2023)
    5. Combine the total number of crimes of assault and property into one single row with the same state name for each year
    6. Normalize crime data per 10,000 population using corresponding year's population data
    """
    
    # Load population data from population_state.csv
    def get_population_data():
        """
        Get population data for each state and year where:
        - sex = both
        - age = overall  
        - ethnicity = overall
        Returns a dictionary with (state, year) as key and population as value
        """
        pop_df = pd.read_csv('multichart/data/map_data/population_state.csv')
        
        # Convert date to datetime
        pop_df['date'] = pd.to_datetime(pop_df['date'])
        pop_df['year'] = pop_df['date'].dt.year
        
        # Filter for the required criteria
        filtered_pop = pop_df[
            (pop_df['sex'] == 'both') &
            (pop_df['age'] == 'overall') &
            (pop_df['ethnicity'] == 'overall')
        ]
        
        print(f"Population data found for {len(filtered_pop)} records")
        print("Years available:", sorted(filtered_pop['year'].unique()))
        print("States found:", sorted(filtered_pop['state'].unique()))
        
        # Convert population to actual numbers (assuming it's in thousands)
        filtered_pop = filtered_pop.copy()
        filtered_pop['population_actual'] = filtered_pop['population'] * 1000
        
        # Create a dictionary mapping (state, year) to population
        population_dict = {}
        for _, row in filtered_pop.iterrows():
            key = (row['state'], row['year'])
            population_dict[key] = row['population_actual']
        
        return population_dict
    
    # Get population data dictionary
    state_year_population = get_population_data()
    
    # Load the CSV file
    df = pd.read_csv('multichart/data/map_data/crime_district.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # 1. Remove rows with state = Malaysia
    df = df[df['state'] != 'Malaysia']
    print(f"After removing Malaysia rows: {df.shape}")
    
    # 2. Remove rows with district != All
    df = df[df['district'] == 'All']
    print(f"After keeping only 'All' districts: {df.shape}")
    
    # 3. Remove rows with type != all
    df = df[df['type'] == 'all']
    print(f"After keeping only 'all' types: {df.shape}")
    
    # 4. Process all years (no filtering by year)
    # Convert date column to datetime and extract year
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    print(f"Processing data for years: {sorted(df['year'].unique())}")
    
    # Check what categories we have
    print(f"Available categories: {df['category'].unique()}")
    
    # 5. Combine the total number of crimes of assault and property for each state and year
    # Filter for only assault and property crimes
    df_filtered = df[df['category'].isin(['assault', 'property'])]
    print(f"After filtering for assault and property: {df_filtered.shape}")
    
    # Group by state and year, sum the crimes
    result = df_filtered.groupby(['state', 'year'])['crimes'].sum().reset_index()
    
    # Add population data for each state and year combination
    result['population'] = result.apply(
        lambda row: state_year_population.get((row['state'], row['year']), None), 
        axis=1
    )
    
    # Remove rows where population data is not available
    missing_pop = result[result['population'].isnull()]
    if len(missing_pop) > 0:
        print(f"\nWarning: Missing population data for {len(missing_pop)} state-year combinations:")
        for _, row in missing_pop.iterrows():
            print(f"  - {row['state']}, {row['year']}")
        
        result = result.dropna(subset=['population'])
        print(f"Removed {len(missing_pop)} rows with missing population data")
    
    # Calculate crimes per 10,000 population
    result['crimes_per_10k_population'] = (result['crimes'] / result['population']) * 10000
    
    # Round to 2 decimal places for cleaner visualization
    result['crimes_per_10k_population'] = result['crimes_per_10k_population'].round(2)
    
    # Create final dataset with state, year, raw crimes, and crimes per 10k population
    final_result = result[['state', 'year', 'crimes', 'crimes_per_10k_population']].copy()
    final_result.columns = ['state', 'year', 'total_crimes', 'crimes_per_10k_population']
    
    # Add helper key combining state and year to aid downstream joins
    final_result['state_year'] = final_result['state'] + '-' + final_result['year'].astype(str)
    
    # Sort by year and then by crimes per 10k population
    final_result = final_result.sort_values(['year', 'crimes_per_10k_population'], ascending=[True, False])
    
    print(f"Final cleaned data shape: {final_result.shape}")
    print(f"\nData available for years: {sorted(final_result['year'].unique())}")
    print(f"Number of states per year: {final_result['year'].value_counts().sort_index()}")
    
    print("\nSample of final cleaned data:")
    print(final_result.head(10))
    
    print("\nTop 5 states with highest crime rates (latest year):")
    latest_year = final_result['year'].max()
    latest_data = final_result[final_result['year'] == latest_year]
    print(latest_data.nlargest(5, 'crimes_per_10k_population')[['state', 'year', 'crimes_per_10k_population']])
    
    # Save the cleaned data with both raw and normalized values
    # Reorder columns for tidy output
    final_result = final_result[['state', 'year', 'state_year', 'total_crimes', 'crimes_per_10k_population']]
    
    final_result.to_csv('multichart/data/map_data/crime_district_cleaned.csv', index=False)
    print(f"\nCleaned data saved to 'multichart/data/map_data/crime_district_cleaned.csv'")
    print(f"Total records: {len(final_result)}")
    
    return final_result

if __name__ == "__main__":
    cleaned_data = clean_crime_data()
