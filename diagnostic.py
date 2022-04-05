from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from db import get_db
import pandas as pd
import json
import sys

HEADER_FILE = sys.argv[1]
CLASSES_FILE = sys.argv[2]

with open(HEADER_FILE) as header_file:
    header_data = json.load(header_file)

MATTER = header_data['matter']
YEAR = header_data['year']
TITLE = header_data['title']
VARS = header_data['vars']
DATA_VALIDATION = header_data['data_validation']
BIMESTRE = header_data['bimestre']
PIXELSIZE = header_data['pixelSize']
METADATA = header_data['metadata']
TEACHERS_CONFIG = header_data['teachers']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS = 'credentials.json' 

class GoogleSheetConnect:
    def __init__(self, credentials):
        self.service = self.connect_service(self.login(credentials))

    def login(self, credentials):
        flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, SCOPES)
        creds = flow.run_local_server(port=0)

        return creds

    def connect_service(self, credentials):
        service = build('sheets', 'v4', credentials=credentials)

        return service

class SpreadsheetService:
    def __init__(self):
        self.service = GoogleSheetConnect(CREDENTIALS).service
        self.spreadsheet = {}

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
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))


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
            ['', header['ano'], header['bimestre'], header['turma'], header['turno']],
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

def get_students(class_id):
    students = pd.read_csv(f'turmas/{class_id}.csv')
    students = students.values
    students.sort(axis=0)
    students =  students.tolist()

    return students

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


def get_classes(file, year='.'):
    classes_df = pd.read_csv(file, na_filter=False)
    columns = classes_df.columns

    classes_df = classes_df[classes_df[columns[1]] == year] if not year == '.' else classes_df
    classes = []

    for i, row in classes_df.iterrows():
        columns = classes_df.columns
        classes.append({
            'class_id': row[columns[0]],
            'year': row[columns[1]],
            'period': row[columns[2]],
            'teacher': row[columns[3]]
        })

    return classes


classes = get_classes(CLASSES_FILE, year=YEAR)

classes = sorted(classes, key=lambda class_item: class_item['class_id'])
class_ids = [class_item['class_id'] for class_item in classes]

spreadsheet_service = SpreadsheetService()
spreadsheet_service.build_spreadsheet(f'FICHA DE {MATTER} {YEAR}', class_ids)

for i, class_obj in enumerate(classes):
    class_id = class_obj['class_id']

    header = {
        'titulo': TITLE,
        'professor': class_obj['teacher'],
        'ano': class_obj['year'],
        'bimestre': BIMESTRE,
        'turma': class_id,
        'turno': class_obj['period'],
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