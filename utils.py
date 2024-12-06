import difflib
import pandas as pd


def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def coloring_coherences(coherences):
    text = ''
    colors = {
        '0': '🟥',
        '1': '🟩',
        '2': '🟦'
    }
    for coherence in coherences:
        text += colors[str(coherence[0])]

    return text


def count_corrects(participants, participant, subject):
    corrects = 0
    answers = getattr(participant, f'TX_RESPOSTAS_{subject}')
    anskey = getattr(participant, f'TX_GABARITO_{subject}')
    language = getattr(participant, 'TP_LINGUA')

    if type(answers) is not str or type(anskey) is not str:
        participants.at[participant.Index, f'NU_CORRETAS_{subject}'] = corrects

        return corrects

    if language == 1 and subject == 'LC':
        anskey = anskey[5:]
    elif language == 0 and subject == 'LC':
        anskey = anskey[:5] + anskey[10:]

    answers = answers.replace('99999', '')
    for i in range(len(answers)):
        if answers[i] == anskey[i]:
            corrects += 1

    participants.at[participant.Index, f'NU_CORRETAS_{subject}'] = corrects

    return corrects


def count_corrects_all(participants: pd.DataFrame, subject):
    participants[f'NU_CORRETAS_{subject}'] = 0

    for participant in participants.itertuples():
        count_corrects(participants, participant, subject)


def coherence(participant, questions: pd.DataFrame, subject,):
    points = getattr(participant, f'NU_NOTA_{subject}')
    answers = getattr(participant, f'TX_RESPOSTAS_{subject}')
    anskey = getattr(participant, f'TX_GABARITO_{subject}')
    language = getattr(participant, 'TP_LINGUA')

    if str(points) == 'nan':
        return points, ([], [], [])
    if language == 1 and subject == 'LC':
        anskey = anskey[5:]
    elif language == 0 and subject == 'LC':
        anskey = anskey[:5] + anskey[10:]

    coer = []
    if type(answers) is not str or type(anskey) is not str:
        return points, ([], [], [])

    parameters = questions[
        questions['CO_PROVA'] == getattr(participant, f'CO_PROVA_{subject}')][[
            'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']].apply(tuple, axis=1
                                                             ).tolist()
    if language == 1 and subject == 'LC':
        parameters = parameters[5:]
    elif language == 0 and subject == 'LC':
        parameters = parameters[:5] + parameters[10:]

    answers = answers.replace('99999', '')
    for i in range(len(answers)):
        coer.append((answers[i] == anskey[i], parameters[i]
                    [0], parameters[i][1], parameters[i][2]))

    coer_a = sorted(coer, key=lambda x: (str(x[1]) == 'nan', x[1]))
    coer_b = sorted(coer, key=lambda x: (str(x[2]) == 'nan', x[2]))
    coer_c = sorted(coer, key=lambda x: (
        str(x[3]) != 'nan', x[3]), reverse=True)

    return points, (coer_a, coer_b, coer_c)


if __name__ == '__main__':
    participants = pd.read_csv(
        '2022/DADOS/MICRODADOS_ENEM_2022_mini.csv', sep=';', encoding='latin1')
    questions = pd.read_csv(
        '2022/DADOS/ITENS_PROVA_2022.csv', sep=';', encoding='latin1')

    count_corrects(participants, 'MT')
    for participant in participants.itertuples():
        print(coherence(participant, questions, 'MT'))
        input()
