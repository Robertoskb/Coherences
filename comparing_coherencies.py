from coherencies import Coherencies
from collections import defaultdict
import matplotlib.pyplot as plt
import exams_codes as ec
from utils import coloring_coherences_str as cc


def check_max_coh(points, coh, current_max, current_coh):
    if points > current_max:
        current_max = points
        current_coh = coh
    return current_max, current_coh


def check_min_coh(points, coh, current_min, current_coh):
    if points < current_min or current_min == 0:
        current_min = points
        current_coh = coh
    return current_min, current_coh


abso = True
year = 2023
subject = 'CN'
path = f'coherences_{year}.csv'
columns = [f'TX_COERENCIA_A_{subject}',
           f'TX_COERENCIA_B_{subject}',
           f'TX_COERENCIA_C_{subject}',
           f'NU_NOTA_{subject}',
           f'NU_CORRETAS_{subject}',
           f'CO_PROVA_{subject}']
coherence = Coherencies.read_coherences(path, columns)

coherence = coherence.sort_values(
    by=f'NU_NOTA_{subject}',)
# coherence = coherence[coherence[f'NU_NOTA_{subject}'] == 650]
# coherence = coherence[coherence[f'NU_CORRETAS_{subject}'] == 30]
coherence = coherence[coherence[f'CO_PROVA_{subject}'].isin(
    ec.codes[year][subject])]
# [min, [sum, count], max]
max_avg_min = defaultdict(lambda: [0, [0, 0], 0])

for c in coherence.itertuples():
    points = getattr(c, f'NU_NOTA_{subject}')
    corrects = getattr(c, f'NU_CORRETAS_{subject}')
    coherence_a = getattr(c, f'TX_COERENCIA_A_{subject}')

    if str(points) == 'nan':
        continue

    if points > max_avg_min[corrects][2]:
        max_avg_min[corrects][2] = points

    if points < max_avg_min[corrects][0] or max_avg_min[corrects][0] == 0:
        max_avg_min[corrects][0] = points

    max_avg_min[corrects][1][0] += points
    max_avg_min[corrects][1][1] += 1

count_start_0 = 0
count_start_1 = 0
points_list_0 = []
points_list_1 = []

absolut_freq_0 = defaultdict(int)
absolut_freq_1 = defaultdict(int)

target = 30

coherence = coherence[coherence[f'NU_CORRETAS_{subject}'] == target]

firsts_cor = 15
target_cor = 12

firsts_inc = 15
target_inc = 8

min_0, max_0, coh_0_min, coh_0_max = 1200, 0, '', ''
min_1, max_1, coh_1_min, coh_1_max = 1200, 0, '', ''
for c in coherence.itertuples():
    points = getattr(c, f'NU_NOTA_{subject}')
    coherence_b = getattr(c, f'TX_COERENCIA_B_{subject}')

    if coherence_b[:firsts_inc].count('0') >= target_inc:
        count_start_0 += 1
        points_list_0.append(points)
        absolut_freq_0[points//5 * 5] += 1

        max_0, coh_0_max = check_max_coh(points, coherence_b, max_0, coh_0_max)
        min_0, coh_0_min = check_min_coh(points, coherence_b, min_0, coh_0_min)

    elif coherence_b[:firsts_cor].count('1') >= target_cor:
        count_start_1 += 1
        points_list_1.append(points)
        absolut_freq_1[points//5 * 5] += 1

        max_1, coh_1_max = check_max_coh(points, coherence_b, max_1, coh_1_max)
        min_1, coh_1_min = check_min_coh(points, coherence_b, min_1, coh_1_min)

if abso:
    label = 'Absolute frequency of participants'
    y_0 = list(absolut_freq_0.values())
    points_list_0 = list(absolut_freq_0.keys())
    y_1 = list(absolut_freq_1.values())
    points_list_1 = list(absolut_freq_1.keys())
else:
    label = 'Cumulative frequency of participants'
    y_0 = list(range(1, count_start_0 + 1))
    y_1 = list(range(1, count_start_1 + 1))

y_max = max_avg_min[target][2]
y_min = max_avg_min[target][0]
y_avg = max_avg_min[target][1][0] / max_avg_min[target][1][1]


plt.figure(figsize=(20, 10))
plt.plot(points_list_0, y_0,
         label=f'{target_inc}+ incorrects in the first {firsts_inc} easy questions', )  # noqa: E501
plt.plot(points_list_1, y_1,
         label=f'{target_cor}+ corrects in the first {firsts_cor} easy questions')  # noqa: E501
plt.axvline(x=y_max, color='r', linestyle='--', label='Max')
plt.axvline(x=y_avg, color='g', linestyle='--', label='Avg')
plt.axvline(x=y_min, color='b', linestyle='--', label='Min')

plt.legend()
plt.xlabel('Points')
plt.ylabel(label)

plt.title(
    f'Points of participants with {target} correct answers in {subject} in the ENEM {year}')  # noqa: E501


plt.figtext(
    0.10, 0.065, f'Maximum points for {target_cor}+ corrects: {max_1}',
    fontsize=10,)
plt.figtext(
    0.10, 0.045, f'{cc(coh_1_max[:firsts_cor])} {cc(coh_1_max[firsts_cor:])}',
    fontsize=10)
plt.figtext(
    0.10, 0.025, f'Minimum points for {target_cor}+ corrects: {min_1}',
    fontsize=10)
plt.figtext(0.10, 0.005,
            f'{cc(coh_1_min[:firsts_cor])} {cc(coh_1_min[firsts_cor:])}',
            fontsize=10)

plt.figtext(
    0.55, 0.065, f'Maximum points for {target_inc}+ incorrects: {max_0}',
    fontsize=10)
plt.figtext(
    0.55, 0.045, f'{cc(coh_0_max[:firsts_inc])} {cc(coh_0_max[firsts_inc:])}',
    fontsize=10)
plt.figtext(
    0.55, 0.025, f'Minimum points for {target_inc}+ incorrects: {min_0}',
    fontsize=10)
plt.figtext(0.55, 0.005,
            f'{cc(coh_0_min[:firsts_inc])} {cc(coh_0_min[firsts_inc:])}',
            fontsize=10)

plt.savefig(
    f'Graphics/{subject}_{target_cor}_{target_inc}{"_abs"if abso else ""}.png')

plt.show()
