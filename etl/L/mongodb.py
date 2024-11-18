from pymongo import MongoClient
import pandas as pd


def load_to_MongoDb(dataframe: pd.DataFrame, nome_db: str = "job-market", nome_collection: str = "jobs"):
    jobs_dict = dataframe.to_dict("records")

    client = MongoClient("mongodb://localhost:27017")
    # select the mongodb database
    db = client[nome_db]

    # get the collection I need to change
    jobs_collection = db[nome_collection]

    # delete the previous data
    jobs_collection.delete_many({})

    # insert the jobs elements
    jobs_collection.insert_many(jobs_dict)


