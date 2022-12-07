import wget
import json

def load_json(file_path):
    with open(file_path, encoding="utf8") as config_file:
        json_file = json.load(config_file)
    return json_file

def build_paramenters(pars):
    build_pars = ''
    for i, k in enumerate(pars):
        if i == 0:
            build_pars += f'{k}={pars[k]}'
        else:
            build_pars += f'&{k}={pars[k]}'
    
    return build_pars

# model = 'https://docs.google.com/spreadsheets/d/[YOUR-ID]/export?format=pdf&portrait=false&size=A4&scale=page'
pars = {
    'format': 'pdf',
    'portrait': 'false',
    'size': 'A4',
    'scale': '4',
    'horizontal_alignment': 'CENTER'
}

tests = load_json('configs/settings_3bim_app.json')['tests']

for t in tests:
    sheet_id = t['link']
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?'
    url = url + build_paramenters(pars)

    print(url)
    wget.download(url)

