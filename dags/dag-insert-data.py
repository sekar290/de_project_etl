from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import json
import psycopg2
import os


from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_container_name = os.getenv("POSTGRES_CONTAINER_NAME")


# Define your Python function to insert data into PostgreSQL
def insert_data_to_postgres():
    # PostgreSQL connection parameters
    db_params = {
        "host": postgres_container_name,
        "database": postgres_db,
        "user":postgres_user,
        "password": postgres_password
    }

    # JSON file path
    json_file_path = "/data/weather-data/weather-20231031.json"

    # Read and parse the JSON data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Adjust the SQL query to match your table's schema
    for record1, record2 in zip(data["hourly"]['time'], data["hourly"]['temperature_2m']):
        cursor.execute(
            "INSERT INTO weather (date_day, temperature) VALUES (%s, %s)",
            (record1, record2)
        )

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Define the default arguments for the DAG
default_args = {
    "owner": "dibimbing",
    "start_date": datetime(2023, 10, 30),
    "retries": 1,
}

# Create the DAG
dag = DAG("json_to_postgres_dag", default_args=default_args, schedule_interval=None)

# Define the task that runs the Python function
insert_data_task = PythonOperator(
    task_id="insert_data_to_postgres_task",
    python_callable=insert_data_to_postgres,
    dag=dag,
)

# Set up the task dependencies
insert_data_task
