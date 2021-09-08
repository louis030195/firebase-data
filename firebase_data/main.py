
from tqdm import tqdm
import json
import fire
from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore_v1.base_client import BaseClient
from google.cloud.firestore_v1 import DocumentReference

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
        for doc in docs:
            d['collection'].append({
                'id': doc[0],
                **doc[1]
            })
        json.dump(d, f, indent=4, default=str)

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