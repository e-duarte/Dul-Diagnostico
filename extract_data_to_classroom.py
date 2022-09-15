import json
import pandas as pd

CONFIG_FILE = 'config_diagnostic.json'

with open(CONFIG_FILE) as config_file:
    ROOM_FILE = json.load(config_file)['students_file']

df_turmas = pd.read_csv(ROOM_FILE)
classrooms = df_turmas['TURMA'].drop_duplicates()[:-2].copy().tolist()
classrooms.sort()

dict_classroom = {
    'classroom':[],
    'grade':[],
    'period': [],
    'teacher':[]
}

for classroom in classrooms:
    dict_classroom['classroom'].append(classroom)
    dict_classroom['grade'].append(int(classroom[1]))
    dict_classroom['period'].append('MANHÃ' if classroom[2] == 'M' else 'TARDE')
    dict_classroom['teacher'].append('')

df_classroom = pd.DataFrame(dict_classroom)
df_classroom.to_csv(f'data/classrooms.csv', index=False)


