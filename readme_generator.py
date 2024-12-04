import os

for i in range(1998, 2024):
    directory = str(i)
    os.makedirs(directory, exist_ok=True)
    readme = f'''Baixe e extraie aqui os arquivos de microdados do ENEM {i} no site do INEP.'''  # noqa: E501
    with open(f'{directory}/README.md', 'w') as f:
        f.write(readme)
