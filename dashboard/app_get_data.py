from dotenv import load_dotenv
import psycopg2
import pandas as pd
import os


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_container_name = os.getenv("POSTGRES_CONTAINER_NAME")
print(f"postgres_user: {postgres_user}")
print(f"postgres_password: {postgres_password}")

class get_data_for_dashboard():

    def get_data_postgres():

        try:
            db_params = {
                "host": postgres_container_name,
                "database": postgres_db,
                "user":postgres_user,
                "password": postgres_password            }

            # Establish a connection to the PostgreSQL database
            print(f"postgres_user: {postgres_user}")
            conn = psycopg2.connect(**db_params)
            print("Connection to PostgreSQL database successful")
            cursor = conn.cursor()

            # query to get data weather from table dim_weather
            query_get_data_weather = """select dw.*, fk.v_name from dim_weather dw
            join fact_kabko fk on fk.n_id_kabko = dw.n_id_kabko 
            """

            cursor.execute(query_get_data_weather)
            row_data_weather = cursor.fetchall()

            df_weather = pd.DataFrame(row_data_weather, columns=[desc[0] for desc in cursor.description])

            # query to get data weather from table dim_air_quality
            query_get_data_air_quality = """select daq.*, fk.v_name from dim_air_quality daq 
            join fact_kabko fk on fk.n_id_kabko = daq.n_id_kabko
            """

            cursor.execute(query_get_data_air_quality)
            row_data_aq = cursor.fetchall()

            df_air_quality = pd.DataFrame(row_data_aq, columns=[desc[0] for desc in cursor.description])

        except Exception as e:
            print("Failed to get data")
        finally:

            # Commit changes and close the connection
            cursor.close()
            conn.close()
        
        return df_weather, df_air_quality