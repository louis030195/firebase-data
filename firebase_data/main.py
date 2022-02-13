import os
from tqdm import tqdm
import json
import fire
import logging
from firebase_admin import credentials, initialize_app, firestore, auth
from google.cloud.firestore_v1.base_client import BaseClient
from google.cloud.firestore_v1 import DocumentReference

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def export_data(
    service_account_path: str, collection: str, output_path: str = "./data",
):
    """
    Export a collection and its data to a json file.
    :param: service_account_path: path to the service account json file
    :param: collection: name of the collection to export
    :param: output_path: path to the output directory
    """
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    docs = []
    # TODO: parallel batches
    for doc in tqdm(f_c.collection(collection).stream()):
        docs.append((doc.id, doc.to_dict()))
        d: DocumentReference = doc.reference
        for sub_collection in d.collections():
            docs[-1][1]["sub_collections"] = {sub_collection.id: []}
            for sub_collection_doc in d.collection(sub_collection.id).stream():
                docs[-1][1]["sub_collections"][sub_collection.id].append(
                    (sub_collection_doc.id, sub_collection_doc.to_dict())
                )
    # Create dir if not exist
    os.makedirs(f"{output_path}", exist_ok=True)
    with open(f"{output_path}/{collection}.json", "w") as f:
        d = {"collection": []}
        for doc in docs:
            d["collection"].append({"id": doc[0], **doc[1]})
        # default=str is used to serialize Firebase timestamps
        json.dump(d, f, indent=4, default=str)
    logger.info(f"{collection} exported")


def import_data(
    service_account_path: str,
    collection: str,
    input_path: str = "./data",
    merge: bool = False,
):
    """
    Import a collection and its data from a json file.
    :param: service_account_path: path to the service account json file
    :param: collection: name of the collection to import
    :param: input_path: path to the input directory
    :param: merge: if True, merge the data with the existing data, otherwise replace it
    """
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    f_c: BaseClient = firestore.client()
    with open(f"{input_path}/{collection}.json", "r") as f:
        d = json.load(f)
        # TODO: parallel batches
        for collection_doc in tqdm(d["collection"]):
            collection_doc_ref = f_c.collection(collection).document(
                collection_doc["id"]
            )
            data = collection_doc
            del data["id"]
            if "sub_collections" in data:
                del data["sub_collections"]
            collection_doc_ref.set(data)
            for sub_collection in collection_doc.get("sub_collections", []):
                for sub_collection_doc in collection_doc["sub_collections"][
                    sub_collection
                ]:
                    collection_doc_ref.collection(sub_collection).document(
                        sub_collection_doc["id"]
                    ).set(sub_collection_doc, merge=merge)
    logger.info(f"{collection} imported")


def export_auth(
    service_account_path: str, output_path: str = "./data",
):
    """
    Export all users and their data to a json file.
    :param: service_account_path: path to the service account json file
    :param: output_path: path to the output directory
    """
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    docs = []
    for doc in tqdm(auth.list_users().iterate_all()):
        docs.append(vars(doc))
    # Create dir if not exist
    os.makedirs(f"{output_path}", exist_ok=True)
    with open(f"{output_path}/users.json", "w") as f:
        json.dump(docs, f, indent=4)
    logger.info("users exported")


def import_auth(
    service_account_path: str, input_path: str = "./data",
):
    """
    Import all users and their data from a json file.
    :param: service_account_path: path to the service account json file
    :param: input_path: path to the input directory
    """
    raise NotImplementedError


def main():
    fire.Fire(
        {
            "export": export_data,
            "import": import_data,
            "auth:export": export_auth,
            "auth:import": import_auth,
        }
    )


if __name__ == "__main__":
    main()
