import json
from datetime import datetime
import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credentials_path = '/home/ewerton/Credentials/service_account_firebase_diagnostic_script.json'
SETTINGS_FILE = 'configs/settings_app.json'
USERS_FILE = 'data/users.csv'


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

def load_users(user_file_path):
    users_df = pd.read_csv(user_file_path)
    columns = users_df.columns.values
    users_formated = []
    print(users_df)
    for i, row in users_df.iterrows():
        users_formated.append({
            'user': row[columns[0]],
            'email': row[columns[1]],
            'manager': row[columns[2]],
            'permission': str(int(row[columns[3]])),
        })
    
    return users_formated

def insert_year_bimester(setting_obj):
    setting_obj['year'] = datetime.now().year
    setting_obj['bimester'] = setting_obj['tests'][0]['bimester']

settings = load_json(SETTINGS_FILE)

# users = load_users(USERS_FILE)

init_firestore()

db = firestore.client()

settings['timestamp'] = datetime.timestamp(datetime.now())

insert_year_bimester(settings)

insert_data('settings', db, settings)

# for u in users:
    # insert_data('users', db, u)

