from pymongo import MongoClient
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import time
from etl.L.firebase import initialize_firestore
from etl.L import *
import re

load_dotenv()
username = os.getenv("USERNAME_SQL")
password = os.getenv("PASSWORD_SQL")
server = os.getenv("SERVER")
db_name = os.getenv("DB_NAME")

# connection to mysql database
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{server}/{db_name}')
conn = engine.connect()

# connection to mongodb database
client = MongoClient("mongodb://localhost:27017")
db_mongodb = client["job-market"]
jobs_collection = db_mongodb["jobs"]

# connection to firestore database
db_firestore = initialize_firestore("../etl/L/credentials.json")

print("Querying MySQL (simple)")
start_time_mysql = time.time()
simple_query_mysql = conn.execute(text("SELECT * FROM company"))
end_time_mysql = time.time()
print(simple_query_mysql)

print("Querying MongoDB (simple)")
start_time_mongodb = time.time()
simple_query_mongodb = jobs_collection.find({}, {"company": 1, "_id": 0})
end_time_mongodb = time.time()
print(simple_query_mongodb)

print("Querying Firestore (simple)")
start_time_firestore = time.time()
jobs_ref = db_firestore.collection("jobs").select(['company'])
jobs_docs = jobs_ref.stream()
end_time_firestore = time.time()
print(jobs_docs)

print("Querying (simple) time in mysql: ", end_time_mysql - start_time_mysql)
print("Querying (simple) time in mongodb: ", end_time_mongodb - start_time_mongodb)
print("Querying (simple) time in firestore: ", end_time_firestore - start_time_firestore)

print("Querying MySQL (complex)")
start_time_mysql = time.time()
complex_query_mysql = conn.execute(text("""
SELECT company.name, location.city, hard_skills.name FROM company_job_skill_location
INNER JOIN location ON location.id = company_job_skill_location.id_location
INNER JOIN company ON company.id = company_job_skill_location.id_company
INNER JOIN hard_skills ON hard_skills.id = company_job_skill_location.id_skill
WHERE location.city = "Roma"
AND hard_skills. name = "SQL"
"""))
end_time_mysql = time.time()
print(complex_query_mysql)

print("Querying MongoDB (complex)")
start_time_mongodb = time.time()
complex_query_mongodb = jobs_collection.find({"location": "Roma", "description": {"$regex": r"\bSQL\b"}})
end_time_mongodb = time.time()


print("Querying Firestore (complex)")
start_time_firestore = time.time()

docs = db_firestore.collection('jobs').where('location', '==', 'Roma').stream()

# Filter results in Python to simulate MongoDB $regex \bSQL\b
pattern = re.compile(r'\bSQL\b', re.IGNORECASE)  # Regex pattern for word boundary
matching_docs = []

for doc in docs:
    description = doc.to_dict().get('description', '')
    if pattern.search(description):
        matching_docs.append(doc.to_dict())

end_time_firestore = time.time()

print("Querying (complex) time in mysql: ", end_time_mysql - start_time_mysql)
print("Querying (complex) time in mongodb: ", end_time_mongodb - start_time_mongodb)
print("Querying (complex) time in firestore: ", end_time_firestore - start_time_firestore)
