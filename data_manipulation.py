import pandas as pd
# import sqlite3
from glob import glob
import mariadb 

# Function to calculate KPI1 and KPI2
def calculate_kpis(input_files):
    # Initialize dataframes for KPIs
    kpi1_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'service_id', 'total_bytes', 'interval'])
    kpi2_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'cell_id', 'number_of_unique_users', 'interval'])
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
            'interval': '5-minute'
        }, ignore_index=True)
    
    # Calculate KPI2: Top 3 cells by number of unique users
    kpi2 = big_df.groupby('cell_id')['msisdn'].nunique().nlargest(3)
    for i in range(len(kpi2.index)):
        kpi2_df = kpi2_df._append({
            'interval_start_timestamp': big_df['interval_start_timestamp'].min(),
            'interval_end_timestamp': big_df['interval_end_timestamp'].max(),
            'cell_id': kpi2.index[i],
            'number_of_unique_users': kpi2.values[i],
            'interval': '5-minute'
        }, ignore_index=True)

    return kpi1_df, kpi2_df

# Function to store KPIs in the database
def store_kpis_in_database(kpi1_df, kpi2_df, database_name='mobile_kpis.db'):
    conn = mariadb.connect(
        user="db_user",
        password="db_user_passwd",
        host="localhost",
        database= database_name)
    with conn.cursor() as cursor:
        try: 
            # Store KPIs in MariaDB
            kpi1_df.to_sql('kpi1_table', cursor, if_exists='append', index=False, method='multi', chunksize=1000)
            kpi2_df.to_sql('kpi2_table', cursor, if_exists='append', index=False, method='multi', chunksize=1000)

        except mariadb.Error as e: 
            print(f"Error: {e}")

        cursor.commit() 
        print(f"Last Inserted ID: {cursor.lastrowid}")
        
   

# Main function
def main():
    # Specify the path to the raw files
    raw_files_path = '/mnt/c/Users/simeo/Desktop/Commsquare_Python_Software_Engineer_Programming_Challenge/**.txt'

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
