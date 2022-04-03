from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017
CONNECTION_STRING = f'mongodb://{HOST}:{PORT}/'

def get_db():
    client = MongoClient(CONNECTION_STRING)
    return client.raimunda

def insert_data(db):
    employees = db.employees
    classes = db.classes
    
    # employees.insert_many(
    #     [
    #         # 3° ANO
    #         {'name':'ELINEIDE DAVI SILVA'},
    #         {'name':'MARIA DO SOCORRO AGUIAR DE PAIVA'},
    #         {'name':'LUCILENE BARBOSA DE LIMA'},
    #         {'name':'ANA PAULA SOUSA DA SILVA'},
    #         {'name': 'MARCELA CRISTINA NASCIMENTO'},
    #         {'name': 'ANDREIA PAIVA FERREIRA'},
    #         {'name': 'MAYARA JUSSARA LEOCÁDIO'},
    #         # 4° ANO
    #         {'name': 'JOSÉ EVANDRO DE SOUSA BEZERRA'},
    #         {'name': 'JAEDNA  BARBOSA DA C. S. DUARTE'},
    #         {'name': 'ROSIENE DA SILVA SANTOS'},
    #         {'name': 'MARIA JOSENILDA LIMA VIEIRA'},
    #         # 5° ANO
    #         {'name': 'PAULO DE SOUZA CASTRO'},
    #     ]
    # )

    # classes.insert_many(
    #     [   
    #         # 3° ANO
    #         {
    #             'class_id':'F3M901',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F3M902',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F3M903',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F3M904',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F3M905',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F3T901',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F3T902',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F3T902',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F3T903',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F3T904',
    #             'year': '3° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         # 4º ANO
    #         {
    #             'class_id':'F4M901',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F4M902',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F4M902',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F4M903',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F4M904',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'MANHÃ',
    #         },
    #         {
    #             'class_id':'F4T901',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F4T902',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F4T903',
    #             'year': '4° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F5M901',
    #             'year': '5° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },
    #         {
    #             'class_id':'F5T901',
    #             'year': '5° ANO',
    #             # 'teacher': S,
    #             'period':'TARDE',
    #         },

    #     ]
    # )

    relations = {
        'ELINEIDE DAVI SILVA': ['F3M901', 'F3T901'],
        'MARIA DO SOCORRO AGUIAR DE PAIVA': ['F3M902', 'F3T902'],
        'LUCILENE BARBOSA DE LIMA': ['F3M903', 'F3T903'],
        'ANA PAULA SOUSA DA SILVA': ['F3M904'],
        'MARCELA CRISTINA NASCIMENTO':['F3M905'],
        'ANDREIA PAIVA FERREIRA':['F3T904'],
        'MAYARA JUSSARA LEOCÁDIO':['F3T905'],
        'JOSÉ EVANDRO DE SOUSA BEZERRA':['F4M901', 'F4T901'],
        'JAEDNA  BARBOSA DA C. S. DUARTE':['F4M902', 'F4T902'],
        'ROSIENE DA SILVA SANTOS':['F4M903'],
        'MARIA JOSENILDA LIMA VIEIRA':['F4T03'],
        'PAULO DE SOUZA CASTRO':['F5M901', 'F5T901'],
    }

    for name in relations:
        employee_id = employees.find_one({'name':name})['_id']
        for class_id in relations[name]:
            classes.update_one({'class_id':class_id}, {'$set':{'employee_id':employee_id}})

def insert_empleyees(db, employees):
    employees_collection = db.employees
    employees_collection.insert_many(employees)

def insert_classes(db, classes):
    classes_collection = db.classes
    classes_collection.insert_many(classes)
    
def insert_relation(db, relations):
    employees = db.employees
    classes = db.classes
    for name in relations:
        employee_id = employees.find_one({'name':name})['_id']
        for class_id in relations[name]:
            classes.update_one({'class_id':class_id}, {'$set':{'employee_id':employee_id}})

if __name__ == '__main__':
    db = get_db()
    # insert_data(dulcineia)

    # for class_obj in dulcineia.classes.find({'year': '3° ANO'}):

    #Professores 1 e 2 ano
    # teachers = [
    #     {'name': 'ADENICELLES MARIA PIRES DA SILVA'},
    #     {'name': 'DILCIVANY BORGES DA SILVA'},
    #     {'name': 'TATIANA MELO SILCA ALVES'},
    #     {'name': 'DINELZA MARIA AMORIM DE CASTRO'},
    #     {'name': 'IRISDALVA ARANHA SOUSA'},
    #     {'name': 'WUYLLENILCE GOMES DOS SANTOS '},
    #     {'name': 'IRISLENE BARBOSA DE LIMA'},
    #     {'name': 'SHEILA DE SOUSA COSTA'},
    #     {'name': 'JOSICLEIA DIAS DOS SANTOS RODRIGUES'},
    #     {'name': 'CRISTIANE DOS SANTOS'},
    #     {'name': 'TAMIRES DE ARAUJO LUIZ'},
    #     {'name': 'MEIRE ROSE GOMES DOS SANTOS '},
    #     {'name': 'FRANCILEIDE SILVA DA CRUZ'},
    #     {'name': 'VANUSA SANTANA SANTOS'},
    #     {'name': 'CLEDDE IRENE SOARES CORREA'},
    #     {'name': 'BENEDITA ELIZANGELA PIRES BARBOSA'},
    # ]

    classes = [
        {
            'class_id':'F6M901-A',
            'year': '6° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F6M902-B',
            'year': '6° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F6T903-C',
            'year': '6° ANO',
            'period':'TARDE',
        },
        {
            'class_id':'F7M901-A',
            'year': '7° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F7M902-B',
            'year': '7° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F7T903-C',
            'year': '7° ANO',
            'period':'TARDE',
        },
        {
            'class_id':'F7T904-D',
            'year': '7° ANO',
            'period':'TARDE',
        },
        {
            'class_id':'F8M901-A',
            'year': '8° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F8M902-B',
            'year': '8° ANO',
            'period':'MANHÃ',
        },
        {
            'class_id':'F8T903-C',
            'year': '8° ANO',
            'period':'TARDE',
        },
        {
            'class_id':'F8T904-D',
            'year': '8° ANO',
            'period':'TARDE',
        },
        {
            'class_id':'F9M901-A',
            'year': '8° ANO',
            'period':'MANHÃ',
        },
        
    ]

    # relations = {
    #     'ADENICELLES MARIA PIRES DA SILVA': ['F1T903'],
    #     'DILCIVANY BORGES DA SILVA': ['F1M904'],
    #     'TATIANA MELO SILCA ALVES': ['F1M905'],
    #     'DINELZA MARIA AMORIM DE CASTRO': ['F1M901', 'F1T901'],
    #     'IRISDALVA ARANHA SOUSA': ['F1M902', 'F1T902'],
    #     'WUYLLENILCE GOMES DOS SANTOS ': ['F2T903'],
    #     'IRISLENE BARBOSA DE LIMA': ['F2M901', 'F2T901'],
    #     'SHEILA DE SOUSA COSTA': ['F2T902'],
    #     'JOSICLEIA DIAS DOS SANTOS RODRIGUES': ['F2T904'],
    #     'CRISTIANE DOS SANTOS': ['F2T905'],
    #     'TAMIRES DE ARAUJO LUIZ': ['F2M904'],
    #     'MEIRE ROSE GOMES DOS SANTOS ': ['F2M903'],
    #     'FRANCILEIDE SILVA DA CRUZ': ['F2M902'],
    #     'VANUSA SANTANA SANTOS': ['F1T904'],
    #     'CLEDDE IRENE SOARES CORREA': ['F1T905'],
    #     'BENEDITA ELIZANGELA PIRES BARBOSA': ['F1M903']
    # }
    # relations = {
    #     'DINELZA MARIA AMORIM DE CASTRO': ['F1T901'],
    # }

    classes = sorted(classes, key=lambda item: item['class_id'])


    # for i in classes:
    #     print(i['class_id'])

    # insert_empleyees(dulcineia, teachers)
    insert_classes(db, classes)
    # insert_relation(dulcineia, relations)