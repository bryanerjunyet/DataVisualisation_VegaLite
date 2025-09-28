import pandas as pd
from datetime import datetime

def clean_crime_data():
    """
    Clean the crime_district.csv data according to specified requirements:
    1. Remove rows with state = Malaysia
    2. Remove rows with district != All
    3. Remove rows with type != all
    4. Remove rows with the date not in the year 2016
    5. Combine the total number of crimes of assault and property into one single row with the same state name
    6. Normalize crime data per 10,000 population (like COVID cases per 10,000 population)
    """
    
    # Load population data from population_state.csv
    def get_population_data():
        """
        Get 2016 population data for each state where:
        - sex = both
        - age = overall  
        - ethnicity = overall
        - date year = 2016
        """
        pop_df = pd.read_csv('population_state.csv')
        
        # Convert date to datetime and filter for 2016
        pop_df['date'] = pd.to_datetime(pop_df['date'])
        pop_df['year'] = pop_df['date'].dt.year
        
        # Filter for the required criteria
        filtered_pop = pop_df[
            (pop_df['year'] == 2016) &
            (pop_df['sex'] == 'both') &
            (pop_df['age'] == 'overall') &
            (pop_df['ethnicity'] == 'overall')
        ]
        
        print(f"Population data found for {len(filtered_pop)} states in 2016")
        print("States found:", filtered_pop['state'].unique())
        
        # Convert population to actual numbers (assuming it's in thousands)
        filtered_pop = filtered_pop.copy()
        filtered_pop['population_actual'] = filtered_pop['population'] * 1000
        
        # Create a dictionary mapping state to population
        return dict(zip(filtered_pop['state'], filtered_pop['population_actual']))
    
    # Get actual population data from CSV
    state_population_2016 = get_population_data()
    

    
    # Load the CSV file
    df = pd.read_csv('crime_district.csv')
    
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
    
    # 4. Remove rows with the date not in the year 2016
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df = df[df['year'] == 2016]
    print(f"After keeping only 2016 data: {df.shape}")
    
    # Check what categories we have
    print(f"Available categories: {df['category'].unique()}")
    
    # 5. Combine the total number of crimes of assault and property for each state
    # Filter for only assault and property crimes
    df_filtered = df[df['category'].isin(['assault', 'property'])]
    print(f"After filtering for assault and property: {df_filtered.shape}")
    
    # Group by state and sum the crimes
    result = df_filtered.groupby('state')['crimes'].sum().reset_index()
    
    # Add population data for each state
    result['population'] = result['state'].map(state_population_2016)
    
    # Calculate crimes per 10,000 population (like COVID cases per 10,000 population)
    result['crimes_per_10k_population'] = (result['crimes'] / result['population']) * 10000
    
    # Round to 2 decimal places for cleaner visualization
    result['crimes_per_10k_population'] = result['crimes_per_10k_population'].round(2)
    
    # Create final dataset with state, raw crimes, and crimes per 10k population
    final_result = result[['state', 'crimes', 'crimes_per_10k_population']].copy()
    final_result.columns = ['state', 'total_crimes', 'crimes_per_10k_population']
    
    print(f"Final cleaned data shape: {final_result.shape}")
    print("\nFinal cleaned data (crimes per 10,000 population - like COVID cases approach):")
    print(final_result.sort_values('crimes_per_10k_population', ascending=False))
    
    # Save the cleaned data with both raw and normalized values
    final_result.to_csv('crime_district_cleaned.csv', index=False)
    print("\nCleaned data saved to 'crime_district_cleaned.csv'")
    
    return final_result

if __name__ == "__main__":
    cleaned_data = clean_crime_data()