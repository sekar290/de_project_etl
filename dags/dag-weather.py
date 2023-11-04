from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json
import os
import psycopg2
import pandas as pd
import csv
from collections import defaultdict

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_container_name = os.getenv("POSTGRES_CONTAINER_NAME")

default_args = {
    "owner": "dibimbing",
    "start_date": datetime(2023, 10, 30),
    "retry_delay": timedelta(minutes=5),
}

# Define your start_date
# start_date = datetime(2023, 10, 30)

with DAG(
    'dag_weather',
    default_args=default_args,
    schedule_interval=None, # This means the DAG is not scheduled, it needs to be triggered manually.
    catchup=False,  # Don't backfill for past dates.
):
    
    def read_kabko():

        try:
            csv_file_path = "/data/lat-long-data/lat_long_data.csv"
            # Read the CSV file into a DataFrame
            # Initialize a dictionary to store the data
            data_dict = defaultdict(list)

            # Open the CSV file
            with open(csv_file_path, mode='r') as csv_file:
                # Create a CSV reader
                csv_reader = csv.DictReader(csv_file)
                
                # Iterate over each row in the CSV file
                for row in csv_reader:
                    for key, value in row.items():
                        data_dict[key].append(value)

        except Exception as e:

            print("Failed read file lat long data")
        
        return data_dict

    def get_data():

        # try:
            
            today = datetime.today()
            formatted_date = today.strftime("%Y-%m-%d")
            formatted_date_file = today.strftime("%Y%m%d")
            year = today.year
            month= today.month

            # Get Param
            # Specify the path
            
            file_path_weather = f"/data/weather-data/weather-{formatted_date_file}.json"
            file_path_air_quality = f"/data/air-quality-data/aq-{formatted_date_file}.json" 
            file_path_weather_csv = f"/data/weather-data/weather-{formatted_date_file}.csv"
            file_path_air_quality_csv = f"/data/air-quality-data/aq-{formatted_date_file}.csv"

            # Call function read_kabko
            data_params = read_kabko()
            id_kabko = data_params['id']
            value_lat = data_params['lat']
            value_long = data_params['long']
            print(f"value_lat: {value_lat}, value_long: {value_long}")

            # Get data weather
            url_weather = "https://api.open-meteo.com/v1/forecast"
            params_weather = {
                "latitude": value_lat,
                "longitude": value_long,
                "hourly": ["temperature_2m", "relativehumidity_2m", "visibility", "uv_index"],
                "forecast_days":1
            }
            # response_weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=-2.9761,-6.6899&longitude=104.7754,108.4751&hourly=temperature_2m,relativehumidity_2m,visibility,uv_index&forecast_days=1')
            response_weather = requests.get(url_weather, params=params_weather)
            
            if response_weather.status_code == 200:
                data_weather = response_weather.json()
                with open(file_path_weather, 'w') as json_file:
                    json.dump(data_weather, json_file, indent=3)

                # Extract values from JSON and create a list of dictionaries
                data_to_write_weather = []
                for a, item in enumerate(data_weather):
                    for i, time in enumerate(item["hourly"]["time"]):
                        data_to_write_weather.append({
                            "n_id_kabko":a+1,
                            "d_date": time,
                            "n_temperature_2m": item["hourly"]["temperature_2m"][i],
                            "n_relativehumidity_2m": item["hourly"]["relativehumidity_2m"][i],
                            "n_visibility": item["hourly"]["visibility"][i],
                            "n_uv_index": item["hourly"]["uv_index"][i]
                        })
                
                # Extract column names from the JSON keys
                column_names = data_to_write_weather[0].keys()
                print(f"column_names: {column_names}")

                # Open the CSV file and write the data
                with open(file_path_weather_csv, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=column_names)
                    writer.writeheader()
                    writer.writerows(data_to_write_weather)
            
            # Get data air quality
            url_air_quality = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params = {
                "latitude": value_lat,
                "longitude": value_long,
                "hourly": ["pm10", "pm2_5"],
                "forecast_days": 1
            }
            # response_air_quality = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=-2.9761,-6.6899&longitude=104.7754,108.4751&hourly=pm10,pm2_5&start_date=2023-11-03&end_date=2023-11-03')
            response_air_quality = requests.get(url_air_quality, params=params)
            if response_weather.status_code == 200:
                data_air_quality = response_air_quality.json()
                with open(file_path_air_quality, 'w') as json_file:
                    json.dump(data_air_quality, json_file, indent=3)
                
                data_to_write_aq = []
                for b, item in enumerate(data_air_quality):
                    for j, time in enumerate(item["hourly"]["time"]):
                        data_to_write_aq.append({
                            "n_id_kabko":b+1,
                            "d_date": item["hourly"]["time"][j],
                            "n_pm10": item["hourly"]["pm10"][j],
                            "n_pm2_5": item["hourly"]["pm2_5"][j]
                        })
                # Extract column names from the JSON keys
                column_names = data_to_write_aq[0].keys()
                print(f"column_names aq: {column_names}")

                # Open the CSV file and write the data
                with open(file_path_air_quality_csv, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=column_names)
                    writer.writeheader()
                    writer.writerows(data_to_write_aq)

        # except Exception as e:
            # print("Failed to write file json")


    def insert_data_to_postgres():

        # try:

            # PostgreSQL connection parameters
            db_params = {
                "host": postgres_container_name,
                "database": postgres_db,
                "user":postgres_user,
                "password": postgres_password
            }

            # JSON file path
            today = datetime.today()
            formatted_date_file = today.strftime("%Y%m%d")
            json_file_path_weather = f"/data/weather-data/weather-{formatted_date_file}.json" 
            json_file_path_air_quality = f"/data/air-quality-data/aq-{formatted_date_file}.json" 
            file_path_weather_csv = f"/data/weather-data/weather-{formatted_date_file}.csv"
            file_path_air_quality_csv = f"/data/air-quality-data/aq-{formatted_date_file}.csv"

            # Read and parse the JSON data
            with open(json_file_path_weather, "r") as json_file_weather:
                data_weather = json.load(json_file_weather)
            with open(json_file_path_air_quality, "r") as json_file_air_quality:
                data_air_quality = json.load(json_file_air_quality)

            print("step this")
            # Establish a connection to the PostgreSQL database
            conn = psycopg2.connect(**db_params)
            print("Connection to PostgreSQL database successful")
            cursor = conn.cursor()

            #     print('insert air quality')

            list_table_name = ['dim_weather', 'dim_air_quality']
            list_file_path = [file_path_weather_csv, file_path_air_quality_csv]
            for table, path_file in zip(list_table_name, list_file_path):
                if table == 'dim_weather':
                    copy_sql = f"""COPY {table} (n_id_kabko, d_date, n_temperature_2m, n_relativehumidity_2m, n_visibility, n_uv_index)
                    FROM stdin DELIMITER AS ',' CSV HEADER;
                                """
                else:
                    copy_sql = f"""COPY {table} (n_id_kabko, d_date, n_pm10, n_pm2_5)
                    FROM stdin DELIMITER AS ',' CSV HEADER;
                                """
                # Open and read the CSV file
                with open(path_file, 'r') as file:
                    cursor.copy_expert(sql=copy_sql, file=file)
                    conn.commit()
                    print("commit csv")
        # except Exception as e:
        #     print("Failed to insert data weather to database postgres")

        # finally:

            # Commit changes and close the connection
            conn.commit()
            cursor.close()
            conn.close()
    
    # Define the tasks in the DAG
    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=get_data,
        provide_context=True
    )

    # Define second task that runs the Python function
    insert_data_task = PythonOperator(
        task_id="insert_data_to_postgres_task",
        python_callable=insert_data_to_postgres
    )

    # Set up the task dependencies
    fetch_data_task >> insert_data_task
    # fetch_data_task
    # insert_data_task