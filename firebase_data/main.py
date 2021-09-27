
import os
from tqdm import tqdm
import json
import fire
from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore_v1.base_client import BaseClient
from google.cloud.firestore_v1 import DocumentReference

def export_data(
    service_account_path,
    collection,
    output_path = './data',
    ):
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    docs = []
    # TODO: parallel batches
    for doc in tqdm(f_c.collection(collection).stream()):
        docs.append((doc.id, doc.to_dict()))
        d: DocumentReference = doc.reference
        for sub_collection in d.collections():
            docs[-1][1]['sub_collections'] = {sub_collection.id: []}
            for sub_collection_doc in d.collection(sub_collection.id).stream():
                docs[-1][1]['sub_collections'][sub_collection.id].append((sub_collection_doc.id, sub_collection_doc.to_dict()))
    # Create dir if not exist
    os.makedirs(f'{output_path}', exist_ok=True)
    with open(f'{output_path}/{collection}.json', 'w') as f:
        d = {'collection': []}
        for doc in docs:
            d['collection'].append({
                'id': doc[0],
                **doc[1]
            })
        # default=str is used to serialize Firebase timestamps
        json.dump(d, f, indent=4, default=str)

def import_data(
    service_account_path,
    collection,
    input_path = './data',
    ):
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    with open(f'{input_path}/{collection}.json', 'r') as f:
        d = json.load(f)
        # TODO: parallel batches
        for collection_doc in tqdm(d['collection']):
            collection_doc_ref = f_c.collection(collection).document(collection_doc['id'])
            data = collection_doc
            del data['id']
            if 'sub_collections' in data: del data['sub_collections']
            collection_doc_ref.set(data)
            for sub_collection in collection_doc.get('sub_collections', []):
                for sub_collection_doc in collection_doc['sub_collections'][sub_collection]:
                    collection_doc_ref.collection(sub_collection).document(sub_collection_doc['id']).set(sub_collection_doc)


def main():
    fire.Fire({
        'export': export_data,
        'import': import_data,
    })

if __name__ == '__main__':
    main()