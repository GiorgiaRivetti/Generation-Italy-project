from mongodb import *
from firebase import *


def mongodb(df):
    # Load df on MongoDB
    load_to_MongoDb(df)


def firestore(df):
    # Load df on Firestore
    db = initialize_firestore()
    delete_data(db, "jobs", 100)
    upload_data(db, "jobs", df)
