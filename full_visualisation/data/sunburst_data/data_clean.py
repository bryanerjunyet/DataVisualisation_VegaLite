import pandas as pd
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the raw crime data from the correct path
input_file = os.path.join(script_dir, 'crime_district.csv')
output_file = os.path.join(script_dir, 'crime_district_cleaned.csv')

print(f"Reading from: {input_file}")
print(f"Writing to: {output_file}")

# Check if input file exists
if not os.path.exists(input_file):
    print(f"Error: Input file {input_file} not found!")
    print("Available files in directory:")
    for file in os.listdir(script_dir):
        if file.endswith('.csv'):
            print(f"  - {file}")
    exit(1)

df = pd.read_csv(input_file)
print(f"Loaded {len(df)} rows from input file")

# Filter for state-level data only (exclude Malaysia, include only states with district='All')
state_data = df[(df['state'] != 'Malaysia') & (df['district'] == 'All')].copy()
print(f"Filtered to {len(state_data)} state-level rows")

# Extract year from date
state_data['year'] = pd.to_datetime(state_data['date']).dt.year

# Function to recategorize crime types
def recategorize_crime_type(crime_type):
    if crime_type == 'all':
        return None  # We'll exclude 'all' entries
    elif crime_type in ['robbery_gang_armed', 'robbery_gang_unarmed']:
        return 'Robbery Gang'
    elif crime_type in ['robbery_solo_armed', 'robbery_solo_unarmed']:
        return 'Robbery Solo'
    elif crime_type in ['theft_vehicle_lorry', 'theft_vehicle_motorcar', 'theft_vehicle_motorcycle']:
        return 'Theft Vehicle'
    elif crime_type == 'causing_injury':
        return 'Causing Injury'
    elif crime_type == 'murder':
        return 'Murder'
    elif crime_type == 'rape':
        return 'Rape'
    elif crime_type == 'break_in':
        return 'Break In'
    elif crime_type == 'theft_other':
        return 'Theft Other'
    else:
        return crime_type.replace('_', ' ').title()

# Apply recategorization
state_data['new_crime_type'] = state_data['type'].apply(recategorize_crime_type)

# Filter out 'all' entries
state_data = state_data[state_data['new_crime_type'].notna()].copy()
print(f"After removing 'all' entries: {len(state_data)} rows")

# Group by year, state, category, and new crime type
grouped = state_data.groupby(['year', 'state', 'category', 'new_crime_type'])['crimes'].sum().reset_index()
print(f"Grouped data has {len(grouped)} rows")

# Create hierarchical structure for sunburst
cleaned_data = []

# Add subcategory entries
for _, row in grouped.iterrows():
    year = row['year']
    state = row['state']
    main_category = row['category'].title()  # assault -> Assault, property -> Property
    sub_category = row['new_crime_type']
    crimes = row['crimes']
    
    cleaned_data.append({
        'Year': year,
        'State': state,
        'Crime_Category': main_category,
        'Crime_Type': sub_category,
        'Cases': crimes,
        'Level': 'Subcategory'
    })

# Create aggregated main category totals by state
main_category_totals = grouped.groupby(['year', 'state', 'category'])['crimes'].sum().reset_index()

for _, row in main_category_totals.iterrows():
    year = row['year']
    state = row['state']
    main_category = row['category'].title()
    crimes = row['crimes']
    
    cleaned_data.append({
        'Year': year,
        'State': state,
        'Crime_Category': main_category,
        'Crime_Type': main_category,  # Same as category for main level
        'Cases': crimes,
        'Level': 'Main'
    })

# Convert to DataFrame
result_df = pd.DataFrame(cleaned_data)

# Sort by Year, State, Level (Main first, then Subcategory), and Crime_Category
result_df = result_df.sort_values(['Year', 'State', 'Level', 'Crime_Category', 'Crime_Type']).reset_index(drop=True)

# Save the cleaned data
result_df.to_csv(output_file, index=False)

print("Data cleaning completed!")
print(f"Total records: {len(result_df)}")
print(f"Output saved to: {output_file}")
print("\nStates included:")
print(sorted(result_df['State'].unique()))
print("\nSample of cleaned data:")
print(result_df.head(15))
print("\nData structure by level:")
print(result_df.groupby(['Level', 'Crime_Category']).size())