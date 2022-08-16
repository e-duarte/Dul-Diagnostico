import json
import os.path

CONFIG_APP_PATH = 'config_app.json'
TESTS_APP_PATH = 'tests_app.json'

def load_json(path):
    json_file = {}
    if os.path.exists(path):
        print(f'opening {path}')

        with open(path, "r", encoding="utf8") as file:
            json_file = json.load(file)
    else:
        print(f'Creating json file to {path}')

        if path.split('_')[0] == 'config':
            config_file = {}

            for m in ['PORTUGUÊS', 'MATEMÁTICA', 'PSICOGÊNESE']:
                config_file[m] = {
                    'rooms': [],
                    'links': []
                }

            with open(path, 'w', encoding="utf8") as file:
                json.dump(config_file, file,  indent=4, ensure_ascii=False)

            json_file = config_file
        else:
            tests_file = {'tests': []}
            
            with open(path, 'w', encoding="utf8") as file:
                json.dump(tests_file, file,  indent=4, ensure_ascii=False)

            json_file = tests_file

    return json_file

def add_link(matter, link):
    element_exist = False

    for l in config_app[matter]['links']:
        if l['link'] == link['link']:
            element_exist = True
    
    if not element_exist:
        config_app[matter]['links'].append(link)

def add_config(matter, rooms, link):
    matter = 'PORTUGUÊS' if (matter == 'LEITURA' or matter == 'LEITURA E ESCRITA') else matter

    config_app[matter]['rooms'].extend(rooms)
    config_app[matter]['rooms'] = list(set(config_app[matter]['rooms']))
    config_app[matter]['rooms'].sort()

    add_link(matter, link)

    print(config_app)

    with open(CONFIG_APP_PATH, 'w', encoding='utf8') as file:
        json.dump(config_app, file,  indent=4, ensure_ascii=False)



def add_test(header):
    if header['matter'] != 'PSICOGÊNESE':

        new_test = {
            'matter': header['matter'],
            'year': int(header['year'][0]),
            'bimestre': header['bimestre'],
            'vars': header['vars'],
            'options': {
                f'var{i+1}': header['data_validation'][i] for i in range(len(header['vars']))
            }
        }
    else:
        new_test = {
            'matter': header['matter'],
            'year': int(header['year'][0]),
            'bimestre': header['bimestre'],
            'vars': 'AVALIAÇÃO DE PSICOGÊNESE',
            'options': {
                f'var{i+1}': header['vars'] for i in range(len(header['vars']))
            }
        }

    print(new_test)

    tests_app['tests'].append(new_test)

    with open(TESTS_APP_PATH, 'w', encoding='utf8') as file:
        json.dump(tests_app, file,  indent=4, ensure_ascii=False)


def add_room_data():
    pass


config_app = load_json(CONFIG_APP_PATH)
tests_app = load_json(TESTS_APP_PATH)




