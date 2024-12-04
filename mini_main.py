import pandas as pd

path = '2022/DADOS/MICRODADOS_ENEM_2022_mini.csv'

df = pd.read_csv(path, sep=';', encoding='latin1', )

for d in df.itertuples():
    print(d.TP_LINGUA)
