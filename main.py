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
    year = 2023
    subject = 'LC'
    path = f'coherences_{year}.csv'
    columns = [f'TX_COERENCIA_A_{subject}',
               f'TX_COERENCIA_B_{subject}',
               f'TX_COERENCIA_C_{subject}',
               f'NU_NOTA_{subject}',
               f'NU_CORRETAS_{subject}',
               f'CO_PROVA_{subject}']
    coherence = Coherences.read_coherences(path, columns)

    coherence = coherence.sort_values(
        by=f'NU_NOTA_{subject}', ascending=False)
    coherence = coherence[coherence[f'NU_NOTA_{subject}'] == 650]
    # coherence = coherence[coherence[f'NU_CORRETAS_{subject}'] == 20]

    for c in coherence.itertuples():
        points = getattr(c, f'NU_NOTA_{subject}')
        corrects = getattr(c, f'NU_CORRETAS_{subject}')
        coherence_a = getattr(c, f'TX_COERENCIA_A_{subject}')
        coherence_b = getattr(c, f'TX_COERENCIA_B_{subject}')
        coherence_c = getattr(c, f'TX_COERENCIA_C_{subject}')

        print(points, corrects, coloring_coherences(coherence_b), end=' ')
        input()
