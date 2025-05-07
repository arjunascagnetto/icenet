import json
import os
import matplotlib.pyplot as plt

# 1) Percorso al file JSON
json_path = 'results/networks/tutorial_testrun/tutorial_testrun_42_history.json'
if not os.path.exists(json_path):
    raise FileNotFoundError(f"File '{json_path}' non trovato.")

# 2) Carica i dati
with open(json_path, 'r') as f:
    data = json.load(f)

# 3) Individua gli step
steps = sorted(
    int(k.replace('binacc', ''))
    for k in data.keys()
    if k.startswith('binacc') and k.replace('binacc','').isdigit()
)

# 4) Prepara le serie
binacc = [data[f'binacc{n}'] for n in steps]
mae    = [data[f'mae{n}']    for n in steps]
rmse   = [data[f'rmse{n}']   for n in steps]

# 5) Crea un'unica figura con 3 subplot
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Binacc
axes[0].plot(steps, binacc, marker='o')
axes[0].set_ylabel('Binacc (%)')
axes[0].set_title('Andamento Binacc')
axes[0].grid(True)

# MAE
axes[1].plot(steps, mae, marker='s')
axes[1].set_ylabel('MAE')
axes[1].set_title('Andamento MAE')
axes[1].grid(True)

# RMSE
axes[2].plot(steps, rmse, marker='^')
axes[2].set_xlabel('Step')
axes[2].set_ylabel('RMSE')
axes[2].set_title('Andamento RMSE')
axes[2].grid(True)

# Regola layout e mostra/salva
plt.xticks(steps)
plt.tight_layout()
plt.savefig('metriche_subplots.png', dpi=300)
plt.show()
