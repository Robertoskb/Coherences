import matplotlib.pyplot as plt
import exams_codes as ec
from collections import defaultdict
from coherencies import Coherencies


year = 2023
path = f'coherences_{year}.csv'
subjects = ['CH', 'CN', 'LC', 'MT']

columns = [f'TX_COERENCIA_B_{subject}' for subject in subjects] + \
    [f'NU_CORRETAS_{subject}' for subject in subjects] + \
    [f'CO_PROVA_{subject}' for subject in subjects]

coherence = Coherencies.read_coherences(path, columns)

for subject in subjects:
    coherence = coherence[coherence[f'CO_PROVA_{subject}'].isin(
        ec.codes[year][subject])]

target = 15
incorrects = 3

count = defaultdict(int)

for c in coherence.itertuples():
    for subject in subjects:
        coherence_b = getattr(c, f'TX_COERENCIA_B_{subject}')

        if str(coherence_b) == 'nan':
            continue

        corrects = getattr(c, f'NU_CORRETAS_{subject}')

        if coherence_b[:target].count('0') >= incorrects:  # noqa: E501
            count[subject, corrects] += 1

x = list(range(46))
y_ch = [count['CH', i] for i in x]
y_cn = [count['CN', i] for i in x]
y_lc = [count['LC', i] for i in x]
y_mt = [count['MT', i] for i in x]

plt.figure(figsize=(12, 6))
plt.plot(x, y_ch, label='CH')
plt.plot(x, y_cn, label='CN')
plt.plot(x, y_lc, label='LC')
plt.plot(x, y_mt, label='MT')

plt.legend()
plt.xlabel('Number of corrects')
plt.ylabel('Number of participants')
plt.title(
    f'Participants with {incorrects}+ incorrects in the first {target} easy questions')  # noqa: E501

plt.savefig(f'Graphics/{incorrects}+ in {target}.png')
print("Done")

plt.show()
