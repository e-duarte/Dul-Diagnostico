import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credentials_path = 'credentials_firebase.json'
CONFIG_FILE = 'config_app.json'
TEST_FILE = 'tests_app.json'

def load_json(file_path):
    with open(file_path, encoding="utf8") as config_file:
        json_file = json.load(config_file)
    return json_file

def init_firestore():
    cred = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(cred, {
        'projectId': 'dulcineia-ee8f1',
    })

def insert_data(collection, db, data):
    doc_ref = db.collection(collection).document()
    doc_ref.set(data)

config = load_json(CONFIG_FILE)
tests = load_json(TEST_FILE)

init_firestore()

db = firestore.client()

config['timestamp'] = datetime.timestamp(datetime.now())
# tests['timestamp'] = datetime.timestamp(datetime.now())


insert_data('configs', db, config)
# insert_data('tests', db, tests)

# tests_ref = db.collection('tests')

# docs = tests_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()["timestamp"]}')