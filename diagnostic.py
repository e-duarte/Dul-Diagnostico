from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import json
from export_data_to_json import add_subject_test, add_classrooms

CONFIG_FILE = 'configs/config_diagnostic.json'

with open(CONFIG_FILE, encoding="utf8") as config_file:
    config = json.load(config_file)

    with open(config['header_file'], encoding="utf8") as header_file:
        header_data = json.load(header_file)
    
CLASSROOMS_FILE = config['classrooms_file']
USERS_FILE = config['users_file']
STUDENTS_FILE = config['students_file']
SUBJECT = header_data['subject']
GRADE = header_data['grade']
TITLE = header_data['title']
VARS = header_data['vars']
DATA_VALIDATION = header_data['data_validation']
BIMESTER = header_data['bimester']
PIXELSIZE = header_data['pixelSize']
METADATA = header_data['metadata']

SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets', ]
# CREDENTIALS = f'{sys._MEIPASS}/credentials.json' 
CREDENTIALS = '/home/ewerton/Credentials/client_secret_api_console_diagnostic_script.json' 


class GoogleSheetConnect:
    def __init__(self, credentials):
        creds = self.login(credentials);
        self.service = self.connect_service(creds)
        self.drive = self.connect_drive(creds)

    def login(self, credentials):
        flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, SCOPES)
        creds = flow.run_local_server(port=0)

        return creds

    def connect_service(self, credentials):
        service = build('sheets', 'v4', credentials=credentials)

        return service
    def connect_drive(self, credentials):
        return build('drive', 'v3', credentials=credentials)

class SpreadsheetService:
    def __init__(self):
        google_connect = GoogleSheetConnect(CREDENTIALS)
        self.service = google_connect.service
        self.drive = google_connect.drive
        self.spreadsheet = {}
    

    def search_folder(self, name):
        page_token = None
        return self.drive.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{name}'",
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name, parents)',
                                         pageToken=page_token).execute()

    def get_id_folder(self):
        response = self.search_folder(f'{BIMESTER}º BIMESTRE')
        folder_id = ''

        for f in response['files']:
            p_id = f['parents'][0]
            parent_response = self.drive.files().get(fileId=p_id,).execute()
            parent_name = parent_response['name']

            if parent_name == METADATA['year']:
                folder_id = f['id']

                
        return folder_id
    
    def move_spreadsheet(self, file_id, folder_id):
        file = self.drive.files().get(fileId=file_id,
                                        fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        file = self.drive.files().update(fileId=file_id,
                                            addParents=folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
    
    def callback(self, request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print(f"Permission Id: {response.get('id')}")

    def share_spreadsheet(self, file_id):
        batch = self.drive.new_batch_http_request(callback=self.callback)
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': METADATA['shared']
        }

        batch.add(self.drive.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
        ))

        batch.execute()

    def build_spreadsheet(self, spreadsheet_title, sheet_titles):

        dimesions = [
            {
                'startRow': 0,
                'startColumn': 0,
                'columnMetadata':[
                    {
                        'pixelSize': 21,
                    }
                ]
            },
            {
                'startRow': 0,
                'startColumn': 1,
                'columnMetadata':[
                    {
                        'pixelSize': 400,
                    }
                ]
            }
        ]

        for i in range(2, 8):
            dimesions.append({
                'startRow': 0,
                'startColumn': i,
                'columnMetadata':[
                    {
                        'pixelSize': PIXELSIZE,
                    }
                ]
            })
        
        spreadsheet = {
            'properties': {
                'title': spreadsheet_title
            },
            
            'sheets': [
                {
                    'properties': {'title': sheet},
                    'data': dimesions,
                }
                for sheet in sheet_titles],
        }

        spreadsheet = self.service.spreadsheets().create(body=spreadsheet,).execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

        folder_id = self.get_id_folder()
        self.move_spreadsheet(spreadsheet_id, folder_id)
        self.share_spreadsheet(spreadsheet_id)

        self.spreadsheet = spreadsheet


    def write(self, range, body):
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet.get('spreadsheetId'),
            range=range,
            valueInputOption='RAW',
            body=body,
        ).execute()

        print('{0} cells updated.'.format(result.get('updatedCells')))

    def format_cells(self, body):
        response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet.get('spreadsheetId'),
                body=body
        ).execute()

def create_template(spreadsheet_service, header, sheet_id):
    sheets = spreadsheet_service.spreadsheet['sheets']
    vars = [var.upper() for var in header['vars']]
    column_len = 5 if 5 > 2 + len(vars) else 2 + len(vars)

    metadata = ['' for i in range(1 + column_len)]
    for i, item in enumerate(['', header['ano'], header['bimestre'], header['turma'], header['turno']]):
        metadata[i] = item

    header_vars = []
    header_vars.append('Nº')
    header_vars.append('ALUNO (A)')

    for i in vars:
        header_vars.append(i)

    body = {
        'values':[
            ['GOVERNO DO ESTADO DO PARÁ'],
            ['PREFEITURA MUNICIPAL DE VITÓRIA DO XINGU'],
            ['SECRETARIA MUNICIPAL DE EDUCAÇÃO'],
            [METADATA['school']],
            [f'INEP: {METADATA["inep"]}'],
            [''],
            [header['titulo']],
            [''],
            [f'PROFESSOR (A) {header["professor"]}'],
            ['', f"{header['ano']}º ANO", f"{header['bimestre']}º BIMESTRE", header['turma'], header['turno']],
            [''],
            header_vars
        ]
    }

    # for i in range(len(header['']))
    spreadsheet_service.write(f'{header["turma"]}!{header["range"]}', body)

    body = {
        'requests': [
            {
                'mergeCells': {
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 0,
                        'endRowIndex': 5,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'mergeType': 'MERGE_ROWS'
                } 
            },
            {
                'mergeCells': {
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 6,
                        'endRowIndex': 7,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'mergeType': 'MERGE_ROWS'
                }
            },
            {
                'mergeCells': {
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 8,
                        'endRowIndex': 9,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'mergeType': 'MERGE_ROWS'
                }
            },

            {
                'updateBorders':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 4,
                        'endRowIndex': 5,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    "bottom": {
                        "style": "SOLID",
                        "width": 1,
                    },
                }
            },
            {
                'updateBorders':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 8,
                        'endRowIndex': 9,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    "top": {
                        "style": "SOLID",
                        "width": 1,
                        # "color": {
                        #     "blue": 1.0
                        # },
                    },
                }
            },
            {
                'updateBorders':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 9,
                        'endRowIndex': 10,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    "bottom": {
                        "style": "SOLID",
                        "width": 1,
                        # "color": {
                        #     "blue": 1.0
                        # },
                    },
                }
            },
            {
                'updateBorders':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 8,
                        'endRowIndex': 10,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    "left": {
                        "style": "SOLID",
                        "width": 1,
                        # "color": {
                        #     "blue": 1.0
                        # },
                    },
                    "right": {
                        "style": "SOLID",
                        "width": 1,
                        # "color": {
                        #     "blue": 1.0
                        # },
                    },
                }
            },
            {
                'repeatCell':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 0,
                        'endRowIndex': 12,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'cell': {
                    'userEnteredFormat': {
                        #    'backgroundColor': {
                        #         'red': 0.0,
                        #         'green': 0.0,
                        #         'blue': 0.0
                        #     },
                        'horizontalAlignment' : 'CENTER',
                            'textFormat': {
                                # 'foregroundColor': {
                                #     'red': 1.0,
                                #     'green': 1.0,
                                #     'blue': 1.0
                                # },
                                'fontSize': 10,
                                # 'bold': True
                            }
                    },
                    },
                    'fields': 'userEnteredFormat(textFormat,horizontalAlignment)'
                }
            },
            {
                'repeatCell':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 6,
                        'endRowIndex': 7,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'cell': {
                        'userEnteredFormat': {
                        
                            'horizontalAlignment' : 'CENTER',
                            'textFormat': {
                                # 'foregroundColor': {
                                #     'red': 1.0,
                                #     'green': 1.0,
                                #     'blue': 1.0
                                # },
                                'fontSize': 12,
                                'bold': True
                            }
                        },
                    },
                    'fields': 'userEnteredFormat(textFormat,horizontalAlignment)'
                }
            },
            {
                'repeatCell':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 11,
                        'endRowIndex': 12,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'cell': {
                    'userEnteredFormat': {
                            'textFormat': {
                                'bold': True
                            }
                    },
                    },
                    'fields': 'userEnteredFormat(textFormat)'
                }
            },
            {
                'repeatCell':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 11,
                        'endRowIndex': 12,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'verticalAlignment' : 'MIDDLE',
                            'wrapStrategy': 'WRAP'
                        },
                    },
                    'fields': 'userEnteredFormat(verticalAlignment, wrapStrategy)'
                }
            },
            {
                'updateBorders':{
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 11,
                        'endRowIndex': 12,
                        'startColumnIndex': 0,
                        'endColumnIndex': column_len,
                    },
                    "top": {
                        "style": "SOLID",
                        "width": 1,
                    },
                    "bottom": {
                        "style": "SOLID",
                        "width": 1,
                    },
                    "left": {
                        "style": "SOLID",
                        "width": 1,
                    },
                    "right": {
                        "style": "SOLID",
                        "width": 1,
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                    },
                }
            },
        ]
    }

    print(body)

    spreadsheet_service.format_cells(body)

def format_student_cells(spreadsheet_service, num_rows, num_columns, sheet_id, num_vars):
    sheets = spreadsheet_service.spreadsheet['sheets']
    body = {
        'requests': [
            {
                'repeatCell':{# formating number cells
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 12,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 0,
                        'endColumnIndex': 1,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'horizontalAlignment' : 'CENTER',
                            'textFormat': {
                                'bold': True
                            },
                            'borders': {
                                'bottom': {
                                    'style': 'SOLID',
                                    'width': 1,
                                },
                                'left': {
                                    'style': 'SOLID',
                                    'width': 1,
                                },
                                'right': {
                                    'style': 'SOLID',
                                    'width': 1,
                                }
                            }
                        },
                    },
                    'fields': 'userEnteredFormat(horizontalAlignment, textFormat, borders)'
                },
            },
            {
                'repeatCell':{# formating text of the students
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 12,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            # 'horizontalAlignment' : 'CENTER',
                            'verticalAlignment' : 'MIDDLE',
                            'wrapStrategy': 'WRAP'                            
                        },
                    },
                    'fields': 'userEnteredFormat(verticalAlignment, wrapStrategy)'
                },
            },
            {
                'repeatCell':{# formating text of vars
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 12,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 2,
                        'endColumnIndex': 2 + num_vars,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'horizontalAlignment' : 'CENTER',
                            'verticalAlignment' : 'MIDDLE',
                            'wrapStrategy': 'WRAP'                            
                        },
                    },
                    'fields': 'userEnteredFormat(horizontalAlignment, verticalAlignment, wrapStrategy)'
                },
            },
            {
                'updateBorders':{ # bottom bordes in final list
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': num_rows - 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 0,
                        'endColumnIndex': num_columns,
                    },
                    'bottom': {
                        'style': 'SOLID',
                        'width': 1,
                    }
                }
            }
        ]
    }

    for i in range(num_vars + 1):
        body['requests'].append({
            'updateBorders':{
                'range': {
                    'sheetId': sheets[sheet_id]['properties']['sheetId'],
                    'startRowIndex': 12,
                    'endRowIndex': num_rows,
                    'startColumnIndex': 0,
                    'endColumnIndex': i + 2,
                },
                'right': {
                    'style': 'SOLID',
                    'width': 1,
                }
            }
        })

    spreadsheet_service.format_cells(body)

def data_validation(spreadsheet_service, num_rows, num_vars, sheet_id, data_values):
    sheets = spreadsheet_service.spreadsheet['sheets']
    body = {
        'requests': [
            {
                'repeatCell':{# data validation
                    'range': {
                        'sheetId': sheets[sheet_id]['properties']['sheetId'],
                        'startRowIndex': 12,
                        'endRowIndex': num_rows,
                        'startColumnIndex': i + 2,
                        'endColumnIndex': i + 2 + 1,
                    },
                    'cell': {
                        'dataValidation': {
                            'condition': {
                                'type': 'ONE_OF_LIST',
                                'values': [
                                    {'userEnteredValue': v}
                                for v in data_values[i]]
                            },
                            'showCustomUi': True,
                        },
                    },
                'fields': 'dataValidation(condition)'
                },
            }
        for i in range(num_vars)]
    }

    spreadsheet_service.format_cells(body)

def get_classrooms(file, grade='.'):
    classrooms_df = pd.read_csv(file, na_filter=False)
    columns = classrooms_df.columns.values

    

    classrooms_df = classrooms_df[classrooms_df[columns[1]] == grade] if not grade == '' else classrooms_df
    dict_classrooms = []

    for i, row in classrooms_df.iterrows():        
        dict_classrooms.append({
            'classroom': row[columns[0]],
            'grade': row[columns[1]],
            'period': row[columns[2]],
            'teacher': row[columns[3]],
        })

    return dict_classrooms

def load_class_students(rooms_path_file):
    class_students_df = pd.read_csv(f'{rooms_path_file}')

    all_rooms = class_students_df['TURMA'].drop_duplicates().copy().tolist()
    all_rooms.sort()
    rooms = all_rooms[2:]
    # rooms = class_students_df['TURMA'].drop_duplicates()[:-2].copy().tolist()

    all_students = {r:(class_students_df[class_students_df['TURMA'] == r]['ALUNOS']).values for r in rooms}

    return all_students

def get_students(class_id):
    class_students = load_class_students(STUDENTS_FILE)

    students = class_students[class_id]
    students.sort()
    for s in students:
        print(s)
    students = [[student] for student in students]

    return students

get_students('F2M905')
exit()

classrooms = get_classrooms(CLASSROOMS_FILE, grade=GRADE)

classrooms = sorted(classrooms, key=lambda class_item: class_item['classroom'])

spreadsheet_service = SpreadsheetService()
spreadsheet_service.build_spreadsheet(
    f'FICHA DE {SUBJECT} {GRADE}',
    [class_item['classroom'] for class_item in classrooms]
)

spreadsheet_id = spreadsheet_service.spreadsheet.get('spreadsheetId')

print('Exporting settings file')
add_subject_test(
    {
        'link': spreadsheet_id,
        'subject': SUBJECT,
        'title': TITLE,
        'grade': GRADE,
        'bimester': BIMESTER,
        'vars': {f'{var}':validation for var, validation in zip(VARS, DATA_VALIDATION)} if SUBJECT != 'PSICOGÊNESE' else {'PSICOGÊNESE':VARS}
    }
)

add_classrooms(classrooms)

users_df = pd.read_csv(USERS_FILE)

for i, classroom_obj in enumerate(classrooms):
    class_id = classroom_obj['classroom']

    teacher_email = classroom_obj['teacher']
    user_serie = users_df.loc[users_df['email'] == teacher_email]
    username = user_serie['user'].values[0]

    header = {
        'titulo': TITLE,
        'professor': username,
        'ano': classroom_obj['grade'],
        'bimestre': BIMESTER,
        'turma': class_id,
        'turno': classroom_obj['period'],
        'vars':  VARS,
    }

    column_range = dict([(-1 * (91 - (i + 26)), chr(i)) for i in range(65, 91)])

    column_len = 5 if 5 > 2 + len(header['vars']) else 2 + len(header['vars'])
    header['range'] = f'A1:{column_range[column_len-1]}12'

    create_template(spreadsheet_service, header, i)
    students = get_students(class_id)
    spreadsheet_service.write(f'{class_id}!A13:A{len(students) + 13}', {'values': [[i+1] for i in range(len(students))]})
    spreadsheet_service.write(f'{class_id}!B13:B{len(students) + 13}', {'values': students})

    format_student_cells(spreadsheet_service, (len(students) - 1) + 13 , column_len, i, len(header['vars']))
    
    if DATA_VALIDATION != []:
        data_validation(spreadsheet_service, (len(students) - 1) + 13, len(header['vars']), i, DATA_VALIDATION)