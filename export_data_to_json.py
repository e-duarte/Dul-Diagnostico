import json
import os.path

SETTINGS_APP_PATH = 'configs/settings_app.json'

def load_json(path):
    settings_file = {}
    if os.path.exists(path):
        print(f'opening {path}')

        with open(path, "r", encoding="utf8") as file:
            settings_file = json.load(file)
    else:
        print(f'Creating json file to {path}')
        settings_file = {
            'tests':[],
            'classrooms': []
        }

    return settings_file

def add_subject_test(test_data):
    new_subjects = list(
        filter(
            lambda subject: test_data['subject'] != subject['subject'] and test_data['grade'] == subject['grade'],
            settings_app['tests']
        )
    )
    new_subjects.append(test_data)

    settings_app['tests'] = new_subjects

    update_json_file(settings_app)
    
def add_classrooms(classrooms_data):
    new_classrooms = settings_app['classrooms']
    for c in classrooms_data:
        new_classrooms = list(
            filter(
                lambda classroom: c['classroom'] != classroom['classroom'], 
                new_classrooms
            )
        )

    new_classrooms.extend(classrooms_data)

    new_classrooms = sorted(new_classrooms, key=lambda class_item: class_item['classroom'])

    settings_app['classrooms'] = new_classrooms;

    update_json_file(settings_app)


def update_json_file(settings_dict):

    with open(SETTINGS_APP_PATH, 'w', encoding='utf8') as file:
            json.dump(settings_dict, file,  indent=4, ensure_ascii=False)

settings_app = load_json(SETTINGS_APP_PATH)




