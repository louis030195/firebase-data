
from tqdm import tqdm
import json
import fire
from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore_v1.base_client import BaseClient
from google.cloud.firestore_v1 import DocumentReference
import datetime

def export_data(
    service_account_path,
    collection,
    ):
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    docs = []
    for doc in tqdm(f_c.collection(collection).stream()):
        docs.append((doc.id, doc.to_dict()))
        d: DocumentReference = doc.reference
        for sub_collection in d.collections():
            docs[-1][1]['sub_collections'] = {sub_collection.id: []}
            for sub_collection_doc in d.collection(sub_collection.id).stream():
                docs[-1][1]['sub_collections'][sub_collection.id].append((sub_collection_doc.id, sub_collection_doc.to_dict()))
    with open(f'data/{collection}.json', 'w') as f:
        d = {'collection': []}
        property_to_timestamp = -1
        for doc in docs:
            # Hack to convert, if needed, DatetimeWithNanoseconds properties to timestamp
            # Typically used in firebase and not JSON serializable
            data = doc[1]
            if property_to_timestamp != None and property_to_timestamp != -1:
                data[property_to_timestamp] = data[property_to_timestamp].timestamp()
            elif property_to_timestamp == -1:
                for k, v in data.items():
                    if issubclass(type(v), datetime.datetime):
                        property_to_timestamp = k
                        data[property_to_timestamp] = data[property_to_timestamp].timestamp()
                if property_to_timestamp == -1:
                    property_to_timestamp = None
            d['collection'].append({
                'id': doc[0],
                **data
            })
        json.dump(d, f, indent=4)

def import_data(
    service_account_path,
    collection
    ):
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    with open(f'data/{collection}.json', 'r') as f:
        d = json.load(f)
        for collection_doc in tqdm(d['collection']):
            collection_doc_ref = f_c.collection(collection).document(collection_doc['id'])
            collection_doc_ref.set(collection_doc)
            for sub_collection in collection_doc.get('sub_collections', []):
                for sub_collection_doc in collection_doc['sub_collections'][sub_collection]:
                    collection_doc_ref.collection(sub_collection).document(sub_collection_doc['id']).set(sub_collection_doc)


def main():
    fire.Fire()

if __name__ == '__main__':
    main()