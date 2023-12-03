import pandas as pd
# import sqlite3
from glob import glob
import mariadb 
from sqlalchemy import create_engine
import datetime
import logging

logging.basicConfig(filename ='app.log', 
                        level = logging.INFO)

def __read_files(input_files):
    df = []
    for file in input_files:
        # Read CSV file into a DataFrame
        df.append(pd.read_csv(file))
    big_df = pd.concat(df, axis=0, ignore_index=True)
    return big_df


def __get_files(date):
    raw_files_path = 'ipflow_data.*.txt'

    format = '%d/%m/%Y'
    input_date = datetime.datetime.strptime(date, format)
    next_day = input_date + datetime.timedelta(days=1)
    timestamp = int(round(input_date.timestamp() * 1000))
    next_day_timestamp = int(round(next_day.timestamp() * 1000))

    result_files = __search_files_in_range(raw_files_path, timestamp, next_day_timestamp)
    logging.info(f"timestamp range:{timestamp}-{next_day_timestamp}")
    return result_files


# Function to calculate KPI1 and KPI2
def __calculate_kpis(big_df, time_interval):
    # Initialize dataframes for KPIs
    kpi1_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'service_id', 'total_bytes', 'interval_period'])
    kpi2_df = pd.DataFrame(columns=['interval_start_timestamp', 'interval_end_timestamp', 'cell_id', 'number_of_unique_users', 'interval_period'])
    
    # Calculate KPI1: Top 3 services by traffic volume
    kpi1 = big_df.groupby('service_id').agg({'bytes_uplink': 'sum', 'bytes_downlink': 'sum'}).sum(axis=1).nlargest(3)
    for i in range(len(kpi1.index)):
        kpi1_df = kpi1_df._append({
            'interval_start_timestamp': big_df['interval_start_timestamp'].min(),
            'interval_end_timestamp': big_df['interval_end_timestamp'].max(),
            'service_id': kpi1.index[i],
            'total_bytes': kpi1.values[i],
            'interval_period': time_interval
        }, ignore_index=True)
    
    # Calculate KPI2: Top 3 cells by number of unique users
    kpi2 = big_df.groupby('cell_id')['msisdn'].nunique().nlargest(3)
    for i in range(len(kpi2.index)):
        kpi2_df = kpi2_df._append({
            'interval_start_timestamp': big_df['interval_start_timestamp'].min(),
            'interval_end_timestamp': big_df['interval_end_timestamp'].max(),
            'cell_id': kpi2.index[i],
            'number_of_unique_users': kpi2.values[i],
            'interval_period': time_interval
        }, ignore_index=True)

    return kpi1_df, kpi2_df

# Function to store KPIs in the database
def __store_kpis_in_database(kpi1_df, kpi2_df):
    engine = create_engine("mariadb+pymysql://root:example@localhost/ETL?charset=utf8mb4")
   
    try: 
        # Store KPIs in MariaDB
        kpi1_df.to_sql('KP1', engine, if_exists='append', index=False, method='multi', chunksize=1000)
        kpi2_df.to_sql('KP2', engine, if_exists='append', index=False, method='multi', chunksize=1000)
        # Enhancment: check for uniqueness of values inserted

    except Exception as e: 
        logging.error(f"Error: {e}")
        
def __search_files_in_range(raw_files_path, start_range, end_range):
    all_files = glob(raw_files_path)
    day_files = [f for f in all_files if f > f"ipflow_data.ts-{start_range}.1.txt" and f < f"ipflow_data.ts-{end_range}.1.txt"]
    logging.info(f"Running for files: {day_files}")
    return day_files


def ETL_operation(time_interval, date):
    # Specify the path to the raw files
    logging.info(f"Running for day {date} with interval {time_interval}")
    result_files = __get_files(date)    

    big_df = __read_files(result_files)
    # Calculate KPIs
    kpi1_df, kpi2_df = __calculate_kpis(big_df, time_interval)
    # Store KPIs in the database
    __store_kpis_in_database(kpi1_df, kpi2_df)



def main():
    time_interval = '5-minute'
    date = "1/3/2017"
    ETL_operation(time_interval, date)   


if __name__ == "__main__":
    main()
