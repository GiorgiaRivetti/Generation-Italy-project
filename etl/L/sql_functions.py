from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

# Connection to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['job-market']
# collection = db['jobs']
#
# # Extract data from MongoDB and transform it into a pandas DataFrame
# data = list(collection.find())
# df = pd.DataFrame(data)

load_dotenv()
username = os.getenv("USERNAME_SQL")
password = os.getenv("PASSWORD_SQL")
server = os.getenv("SERVER")
db_name = os.getenv("DB_NAME")


def mysql(df):
    # Connect to MySQL without specifying a database initially
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{server}')
    conn = engine.connect()

    # Create the database if it doesn't exist
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    # Switch to the created or existing database
    conn.execute(text(f"USE {db_name}"))

    # Bind the engine to the new database
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{server}/{db_name}')
    metadata = MetaData()

    # Definition of the main tables
    job_title = Table('job_title', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('title', String(255), nullable=False)
                      )

    hard_skills = Table('hard_skills', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('name', String(255), nullable=False)
                        )

    company = Table('company', metadata,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('name', String(255), nullable=False)
                    )

    location = Table('location', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('city', String(255), nullable=False),
                     Column('province', String(255), nullable=False),
                     Column('region', String(255), nullable=False),
                     Column('area', String(255), nullable=False),
                     )

    # Definition of relational table with location_id included
    company_job_skill = Table('company_job_skill_location', metadata,
                              Column('id', Integer, primary_key=True, autoincrement=True),
                              Column('id_job_title', Integer, ForeignKey('job_title.id')),
                              Column('id_company', Integer, ForeignKey('company.id')),
                              Column('id_skill', Integer, ForeignKey('hard_skills.id')),
                              Column('id_location', Integer, ForeignKey('location.id'))  # Added location ID here
                              )

    # Drop all existing tables
    metadata.drop_all(engine)
    # Create all the tables defined in the metadata object
    metadata.create_all(engine)

    # Create a session to allow data entry
    Session = sessionmaker(bind=engine)
    session = Session()

    # Data entry for all the main tables
    for title in df['title'].unique():
        session.execute(job_title.insert().values(title=title))

    for company_name in df['company'].unique():
        session.execute(company.insert().values(name=company_name))

    city_list = []

    for index, row in df.iterrows():
        # Insert values into table 'location'
        if str(row['location']) not in city_list:
            city_list.append(str(row['location']))

            session.execute(location.insert().values(
                city=row['location'] if pd.notna(row['location']) else None,
                province=row['province'] if pd.notna(row['province']) else None,
                region=row['region'] if pd.notna(row['region']) else None,
                area=row['area'] if pd.notna(row['area']) else None
            ))

    # Separate the skills and remove spaces
    def extract_skills(description):
        return [skill.strip() for skill in description.split(',')]

    # Create a dict to map id_job_title, id_company, id_skill, id_location
    job_title_ids = {title: id for id, title in session.execute(text('SELECT id, title FROM job_title'))}
    company_ids = {company_name: id for id, company_name in session.execute(text('SELECT id, name FROM company'))}
    location_ids = {city: id for id, city in session.execute(text('SELECT id, city FROM location'))}

    # Dict to memorize the skills already inserted and avoid duplicates
    skill_ids = {}

    # Insert data into relational table company_job_skill and insert the skills into skills table
    for index, row in df.iterrows():
        job_id = job_title_ids[row['title']]
        company_id = company_ids[row['company']]
        location_id = location_ids.get(row['location'])  # Get the location ID

        # Split the skills in the "description" field
        skills_list = extract_skills(row['description'])

        for skill in skills_list:
            # Insert the skill in the skill_ids dictionary ({"skill": "id"} format) if it does not exist
            if skill not in skill_ids:
                result = session.execute(
                    hard_skills.insert().values(name=skill))  # insert the skill in the hard_skills table
                session.commit()  # commit the insertion
                skill_ids[skill] = result.lastrowid  # get the id of the skill just entered (auto-increment id)

            skill_id = skill_ids[skill]

            # Check if the combination of job, company, skill, and location already exists in company_job_skill
            existing_entry = session.query(company_job_skill).filter_by(
                id_job_title=job_id,
                id_company=company_id,
                id_skill=skill_id,
                id_location=location_id  # Include location ID in the check
            ).first()

            if existing_entry is None:
                # Insert the relation between job, company, skill, and location into the relational table
                session.execute(
                    company_job_skill.insert().values(id_job_title=job_id, id_company=company_id,
                                                      id_skill=skill_id,
                                                      id_location=location_id)  # Insert location ID here
                )

    session.commit()
