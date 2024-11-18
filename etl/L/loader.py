import time
from nosql_functions import mongodb, firestore
from sql_functions import mysql
import pandas as pd
from etl.ET.job_processor import *
from dotenv import load_dotenv
import os

# # Create final_df and export to jobs
# load_dotenv()
# assets_folder = os.getenv('ASSETS_FOLDER')
# 
# df = get_final_df(f'../{assets_folder}/all_jobs.json')
# 
# json_output = df.to_json("standardized_jobs.json")

df = pd.read_json("standardized_jobs.json")

# Loading performance_test
start_time_mongodb = time.time()
print("Uploading on MongoDB")
mongodb(df)
end_time_mongodb = time.time()

start_time_firestore = time.time()
print("Uploading on Firestore")
firestore(df)
end_time_firestore = time.time()

start_time_mysql = time.time()
print("Uploading on MySQL")
mysql(df)
end_time_mysql = time.time()

print("Tempo per caricamento in mongodb: ", end_time_mongodb - start_time_mongodb)
print("Tempo per caricamento in firestore: ", end_time_firestore - start_time_firestore)
print("Tempo per caricamento in mysql: ", end_time_mysql - start_time_mysql)
