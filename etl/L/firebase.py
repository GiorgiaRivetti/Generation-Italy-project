import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import concurrent.futures


# Initialize Firestore DB
def initialize_firestore(credentials_json='credentials.json'):
    # Path to the downloaded service account key JSON file
    cred = credentials.Certificate(credentials_json)
    firebase_admin.initialize_app(cred)
    return firestore.client()


def delete_data(db, collection_name, batch_size):
    ref = db.collection(collection_name)

    while True:
        # Retrieve a batch of documents
        docs = ref.limit(batch_size).stream()
        deleted = 0

        def delete_doc(doc):
            # print(f"Deleting doc {doc.id} from {collection_name}")
            doc.reference.delete()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(delete_doc, doc) for doc in docs]

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                deleted += 1

        # Break the loop if no more documents to delete
        if deleted < batch_size:
            break


def download_data(db, collection_name):
    # Retrieve data from Firestore
    ref = db.collection(collection_name)
    docs = ref.stream()  # Extracts all documents from the collection

    # Turns every document into a dictionary
    # **x.to_dict() -> Extracts each key-value pair
    items = list(map(lambda x: {**x.to_dict()}, docs))

    df = pd.DataFrame(items)
    return df


def upload_data(db, collection_name, df):
    def upload_row(index, row):
        doc_id = str(index)
        data = row.to_dict()
        db.collection(collection_name).document(doc_id).set(data)
        # print(f"Data uploaded to {collection_name}/{doc_id}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(upload_row, index, row) for index, row in df.iterrows()]

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise exceptions if any occurred during upload
