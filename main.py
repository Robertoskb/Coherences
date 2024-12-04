import pandas as pd
from utils import coloring_coherences


class Coherences:
    def __init__(self, data):
        self.data = data

    @classmethod
    def read_coherences(cls, path, columns):
        print("Reading participants from file: ", path)
        df = pd.read_csv(path, sep=';', encoding='latin1', usecols=columns)
        print("Participants read successfully")

        return df


if __name__ == "__main__":
    year = 2021
    path = f'coherences_{year}.csv'
    columns = ['TX_COERENCIA_MT', 'NU_NOTA_MT', 'NU_CORRETAS_MT']

    coherence = Coherences.read_coherences(path, columns)

    coherence = coherence.sort_values(by='NU_NOTA_MT', ascending=False)
    coherence = coherence[coherence['NU_NOTA_MT'] == 800]

    for c in coherence.itertuples():
        print(c.NU_NOTA_MT, coloring_coherences(c.TX_COERENCIA_MT))
        input()
