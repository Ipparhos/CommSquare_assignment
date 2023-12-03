import pandas as pd
# import sqlite3
from glob import glob
import mariadb 
from sqlalchemy import create_engine

# Function to calculate KPI1 and KPI2
def calculate_kpis(input_files):
    # Initialize dataframes for KPIs
    kpi1_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'service_id', 'total_bytes', 'interval_period'])
    kpi2_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'cell_id', 'number_of_unique_users', 'interval_period'])
    df = []
    for file in input_files:
        # Read CSV file into a DataFrame
        df.append(pd.read_csv(file))
    big_df = pd.concat(df, axis=0, ignore_index=True)
    # print(big_df)
    # Calculate KPI1: Top 3 services by traffic volume
    kpi1 = big_df.groupby('service_id').agg({'bytes_uplink': 'sum', 'bytes_downlink': 'sum'}).sum(axis=1).nlargest(3)
    # print(kpi1)
    for i in range(len(kpi1.index)):
        kpi1_df = kpi1_df._append({
            'interval_start_timestamp': big_df['interval_start_timestamp'].min(),
            'interval_end_timestamp': big_df['interval_end_timestamp'].max(),
            'service_id': kpi1.index[i],
            'total_bytes': kpi1.values[i],
            'interval_period': '5-minute'
        }, ignore_index=True)
    
    # Calculate KPI2: Top 3 cells by number of unique users
    kpi2 = big_df.groupby('cell_id')['msisdn'].nunique().nlargest(3)
    for i in range(len(kpi2.index)):
        kpi2_df = kpi2_df._append({
            'interval_start_timestamp': big_df['interval_start_timestamp'].min(),
            'interval_end_timestamp': big_df['interval_end_timestamp'].max(),
            'cell_id': kpi2.index[i],
            'number_of_unique_users': kpi2.values[i],
            'interval_period': '5-minute'
        }, ignore_index=True)

    return kpi1_df, kpi2_df

# Function to store KPIs in the database
def store_kpis_in_database(kpi1_df, kpi2_df):
    engine = create_engine("mariadb+pymysql://root:example@localhost/ETL?charset=utf8mb4")
   
    try: 
        # Store KPIs in MariaDB
        kpi1_df.to_sql('KP1', engine, if_exists='append', index=False, method='multi', chunksize=1000)
        kpi2_df.to_sql('KP2', engine, if_exists='append', index=False, method='multi', chunksize=1000)
        # Enhancment: check for uniqueness of values inserted

    except mariadb.Error as e: 
        print(f"Error: {e}")
        
   

# Main function
def main():
    # Specify the path to the raw files
    raw_files_path = '**.txt'

    # Get a list of all raw files
    raw_files = glob(raw_files_path)
    print(raw_files)

    # Calculate KPIs
    kpi1_df, kpi2_df = calculate_kpis(raw_files)
    print(f'kpi1_df:{kpi1_df}')
    print(f'kpi2_df:{kpi2_df}')
    # Store KPIs in the database
    store_kpis_in_database(kpi1_df, kpi2_df)

if __name__ == "__main__":
    main()
