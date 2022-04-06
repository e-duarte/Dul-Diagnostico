import json
import pandas as pd
import os

CONFIG_FILE = 'config.json'

with open(CONFIG_FILE) as config_file:
    ROOM_FILE = json.load(config_file)['rooms_file']

df_turmas = pd.read_csv(ROOM_FILE)
classes = df_turmas['TURMA'].drop_duplicates()[:-2].copy().tolist()
classes.sort()

for c in classes:
    turma = df_turmas[df_turmas['TURMA'] == c]['ALUNOS']

    if not os.path.exists('turmas/'):
        os.mkdir('./turmas')

    turma.to_csv(f'turmas/{c}.csv', index=False)
    print(turma)

