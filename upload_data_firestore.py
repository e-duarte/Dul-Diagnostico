import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credentials_path = '/home/ewerton/Credentials/service_account_firebase_diagnostic_script.json'
SETTINGS_FILE = 'settings_app.json'

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

settings = load_json(SETTINGS_FILE)

init_firestore()

db = firestore.client()

settings['timestamp'] = datetime.timestamp(datetime.now())

insert_data('settings', db, settings)

