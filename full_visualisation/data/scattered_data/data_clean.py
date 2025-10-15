import pandas as pd
import os

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read the crime data
    crime_df = pd.read_csv(os.path.join(script_dir, 'crime_district_cleaned.csv'))
    
    # Read the unemployment data
    unemployment_df = pd.read_csv(os.path.join(script_dir, 'unemployment_state.csv'))
    
    # Clean column names by stripping whitespace
    unemployment_df.columns = unemployment_df.columns.str.strip()
    
    print("Crime data columns:", crime_df.columns.tolist())
    print("Unemployment data columns:", unemployment_df.columns.tolist())
    print("\nSample crime data:")
    print(crime_df.head())
    print("\nSample unemployment data:")
    print(unemployment_df.head())
    
    # Clean state names in unemployment data to match crime data format
    def normalize_state_name(state):
        state = str(state).strip()
        # Replace "W.P " with "W.P. " to match crime data format
        if state.startswith('W.P '):
            return state.replace('W.P ', 'W.P. ')
        return state
    
    unemployment_df['State/Country'] = unemployment_df['State/Country'].apply(normalize_state_name)
    
    # Rename columns for clarity
    unemployment_df = unemployment_df.rename(columns={
        'State/Country': 'state',
        'Year': 'year',
        'Unemployment Rate (Percentage)': 'unemployment_rate'
    })
    
    # Remove any leading/trailing spaces from state names
    crime_df['state'] = crime_df['state'].str.strip()
    unemployment_df['state'] = unemployment_df['state'].str.strip()
    
    # Convert unemployment_rate to numeric, handling any string values
    unemployment_df['unemployment_rate'] = pd.to_numeric(unemployment_df['unemployment_rate'], errors='coerce')
    
    print("\nUnique states in crime data:", sorted(crime_df['state'].unique()))
    print("\nUnique states in unemployment data:", sorted(unemployment_df['state'].unique()))
    
    # Merge the dataframes on state and year
    merged_df = pd.merge(
        crime_df,
        unemployment_df[['state', 'year', 'unemployment_rate']],
        on=['state', 'year'],
        how='inner'
    )
    
    # Select only the required columns
    result_df = merged_df[['state', 'year', 'total_crimes', 'crimes_per_10k_population', 'unemployment_rate']]
    
    # Sort by year and state
    result_df = result_df.sort_values(['year', 'state']).reset_index(drop=True)
    
    # Save to CSV
    output_path = os.path.join(script_dir, 'crime_unemployment_state.csv')
    result_df.to_csv(output_path, index=False)
    
    print(f"\nData cleaning completed!")
    print(f"Output saved to: {output_path}")
    print(f"Total records: {len(result_df)}")
    print("\nSample of merged data:")
    print(result_df.head(10))
    print("\nData summary by year:")
    print(result_df.groupby('year').size())

if __name__ == "__main__":
    main()
