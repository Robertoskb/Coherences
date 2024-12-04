import pandas as pd
from utils import count_corrects


class Participants:

    def __init__(self, data):
        self.data = data

    @classmethod
    def read_participants(cls, path, columns):
        print("Reading participants from file: ", path)
        df = pd.read_csv(path, sep=';', encoding='latin1', usecols=columns)
        print("Participants read successfully")

        return df


if __name__ == "__main__":
    path = "2021/DADOS/MICRODADOS_ENEM_2021.csv"
    columns = ['NU_INSCRICAO', 'NU_NOTA_MT', 'TX_RESPOSTAS_MT',
               'TX_GABARITO_MT', 'CO_PROVA_MT', 'NO_MUNICIPIO_ESC']

    participants = Participants.read_participants(path, columns)
    participants['CORRECTS'] = 0

    count_corrects(participants)

    participants = participants.sort_values(by='NU_NOTA_MT', ascending=False)

    print(participants[participants['NO_MUNICIPIO_ESC'] == 'Tibau'])
