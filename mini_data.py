import pandas as pd


def mini_data(year: int, n: int):
    path = f'{year}/DADOS/MICRODADOS_ENEM_{year}.csv'
    data = pd.read_csv(path, nrows=n, sep=';', encoding='latin1')
    data.to_csv(f'{year}/DADOS/MICRODADOS_ENEM_{year}_mini.csv',
                index=False, sep=';', encoding='latin1')


mini_data(2022, 1000)
