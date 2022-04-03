import pandas as pd

df_turmas = pd.read_csv('turmas/turmas-raimunda.csv')
classes = df_turmas['TURMA'].drop_duplicates()[:-2].copy().tolist()
classes.sort()

for c in classes:
    turma = df_turmas[df_turmas['TURMA'] == c]['ALUNOS']
    turma.to_csv(f'turmas/{c}.csv', index=False)
    print(turma)

