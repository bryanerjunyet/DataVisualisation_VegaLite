import pandas as pd
import os

def clean_crime_district_data():
    # Read the crime district data - use relative path from project root
    try:
        input_path = 'full_visualisation/data/bar_data/crime_district.csv'
        df = pd.read_csv(input_path)
        print(f"Successfully read {input_path}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
        print("Please ensure the crime_district.csv file is in the full_visualisation/data/bar_data/ folder.")
        return
    
    # Filter for Malaysia national data (state='Malaysia', district='All') and required categories
    df_filtered = df[(df['state'] == 'Malaysia') & 
                     (df['district'] == 'All') & 
                     (df['category'].isin(['assault', 'property']))]
    
    print(f"Filtered data shape: {df_filtered.shape}")
    
    # Extract year from date column
    df_filtered = df_filtered.copy()
    df_filtered['Year'] = pd.to_datetime(df_filtered['date']).dt.year
    
    # Group by Year and category, sum the crimes
    df_grouped = df_filtered.groupby(['Year', 'category'])['crimes'].sum().reset_index()
    
    # Rename columns to match expected output format
    df_grouped = df_grouped.rename(columns={'category': 'Crime_Type', 'crimes': 'Cases'})
    
    # Capitalize Crime_Type values for consistency
    df_grouped['Crime_Type'] = df_grouped['Crime_Type'].str.capitalize()
    
    # Ensure we have data for both crime types for each year
    years = sorted(df_grouped['Year'].unique())
    complete_data = []
    
    for year in years:
        year_data = df_grouped[df_grouped['Year'] == year]
        
        # Initialize counts
        assault_count = 0
        property_count = 0
        
        # Extract counts for each crime type
        for _, row in year_data.iterrows():
            if row['Crime_Type'] == 'Assault':
                assault_count = row['Cases']
            elif row['Crime_Type'] == 'Property':
                property_count = row['Cases']
        
        # Add rows for both crime types (even if count is 0)
        complete_data.append({'Year': year, 'Crime_Type': 'Assault', 'Cases': assault_count})
        complete_data.append({'Year': year, 'Crime_Type': 'Property', 'Cases': property_count})
    
    # Create final dataframe
    df_clean = pd.DataFrame(complete_data)
    
    # Sort by year and crime type for consistency
    df_clean = df_clean.sort_values(['Year', 'Crime_Type']).reset_index(drop=True)
    
    # Save cleaned data to the same directory as the script
    output_path = 'full_visualisation/data/bar_data/crime_district_cleaned.csv'
    df_clean.to_csv(output_path, index=False)
    
    print(f"Cleaned data saved to {output_path}")
    print(f"Final data shape: {df_clean.shape}")
    print("\nData preview:")
    print(df_clean.head(10))
    print("\nData summary by crime type:")
    print(df_clean.groupby('Crime_Type')['Cases'].agg(['count', 'sum', 'mean']))
    print("\nYear range:", df_clean['Year'].min(), "to", df_clean['Year'].max())

if __name__ == "__main__":
    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    print("Looking for files in full_visualisation/data/bar_data/:")
    
    bar_data_path = 'full_visualisation/data/bar_data/'
    if os.path.exists(bar_data_path):
        files = [f for f in os.listdir(bar_data_path) if f.endswith('.csv')]
        for file in files:
            print(f"  - {file}")
    else:
        print("  Directory not found!")
    print()
    
    clean_crime_district_data()