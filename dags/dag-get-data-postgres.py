from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import json
import psycopg2
import os