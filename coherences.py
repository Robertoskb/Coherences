from utils import coherence, count_corrects
from participants import Participants
from questions import Questions
import csv
import time


def tx_coherence(coherence):
    text = ''
    for c in coherence:
        if str(c[1]) != 'nan':
            text += ('1' if c[0] else '0')
        else:
            text += '2'
    return text


year = '2023'
subjects = ['MT', 'CH', 'CN', 'LC']

participants_path = f"{year}/DADOS/MICRODADOS_ENEM_{year}.csv"
questions_path = f'{year}/DADOS/ITENS_PROVA_{year}.csv'

collumns_participants = ['NU_INSCRICAO',
                         'NU_NOTA_MT', 'TX_RESPOSTAS_MT',
                         'TX_GABARITO_MT', 'CO_PROVA_MT',

                         'NU_NOTA_CH', 'TX_RESPOSTAS_CH',
                         'TX_GABARITO_CH', 'CO_PROVA_CH',

                         'NU_NOTA_CN', 'TX_RESPOSTAS_CN',
                         'TX_GABARITO_CN', 'CO_PROVA_CN',

                         'NU_NOTA_LC', 'TX_RESPOSTAS_LC',
                         'TX_GABARITO_LC', 'CO_PROVA_LC',
                         'TP_LINGUA']

start = time.time()
participants = Participants.read_participants(
    participants_path, collumns_participants)

collumns_questions = ['CO_POSICAO', 'SG_AREA',
                      'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'CO_PROVA']
questions = Questions.read_questions(questions_path, collumns_questions)


def generate_data(participants, subjects, questions):
    for participant in participants.itertuples():
        row = {'TP_LINGUA': participant.TP_LINGUA}
        for subject in subjects:
            corrects = count_corrects(participants, participant, subject)
            points, coer = coherence(participant, questions, subject)
            tx_coherence_a = tx_coherence(coer[0])
            tx_coherence_b = tx_coherence(coer[1])
            tx_coherence_c = tx_coherence(coer[2])

            row.update({
                f'NU_NOTA_{subject}': points,
                f'NU_CORRETAS_{subject}': corrects,
                f'TX_COERENCIA_A_{subject}': tx_coherence_a,
                f'TX_COERENCIA_B_{subject}': tx_coherence_b,
                f'TX_COERENCIA_C_{subject}': tx_coherence_c,
                f'CO_PROVA_{subject}': getattr(participant,
                                               f'CO_PROVA_{subject}')
            })
        yield row


def write_data_to_csv(generator, output_path, fieldnames):
    with open(output_path, mode='w', encoding='latin1', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in generator:
            writer.writerow(row)


data = generate_data(participants, subjects, questions)

fieldnames = (
    ['TP_LINGUA'] +
    [f'NU_NOTA_{s}' for s in subjects] +
    [f'NU_CORRETAS_{s}' for s in subjects] +
    [f'TX_COERENCIA_A_{s}' for s in subjects] +
    [f'TX_COERENCIA_B_{s}' for s in subjects] +
    [f'TX_COERENCIA_C_{s}' for s in subjects] +
    [f'CO_PROVA_{s}' for s in subjects]
)

output_path = f'coherences_{year}.csv'
write_data_to_csv(data, output_path, fieldnames)

print(time.time() - start)
