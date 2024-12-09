import pandas as pd


class Questions:

    def __init__(self, data):
        self.data = data

    @classmethod
    def read_questions(cls, path, columns):
        print("Reading questions from file: ", path)
        df = pd.read_csv(path, sep=';', encoding='latin1', usecols=columns)
        print("Questions read successfully")

        return df


if __name__ == '__main__':
    path = '2023/DADOS/ITENS_PROVA_2023.csv'
    columns = ['CO_POSICAO', 'SG_AREA', 'NU_PARAM_B', 'CO_PROVA']
    questions = Questions.read_questions(path, columns)

    questions = questions.sort_values(by='NU_PARAM_B')
    questions = questions[questions['SG_AREA'] == 'MT']
    questions = questions[questions['CO_PROVA'] == 1214]

    for q in questions.itertuples():
        print(q.CO_POSICAO, q.NU_PARAM_B)
