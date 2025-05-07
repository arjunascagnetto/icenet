import json
import os
import matplotlib.pyplot as plt

# 1) Percorso al file JSON
json_path = 'results/networks/tutorial_testrun/tutorial_testrun.model_tutorial_data.42.results.json'

# Verifica che il file esista
if not os.path.exists(json_path):
    raise FileNotFoundError(f"File '{json_path}' non trovato. Controlla il percorso.")

# 2) Carica il JSON
with open(json_path, 'r') as f:
    data = json.load(f)

# 3) Stampa diagnostica delle chiavi
print("Chiavi trovate nel JSON:", list(data.keys()))

# 4) Costruisci la lista degli step basandoti sulle chiavi 'binaccN'
steps = sorted(
    int(k.replace('binacc', ''))
    for k in data.keys()
    if k.startswith('binacc') and k.replace('binacc','').isdigit()
)

if not steps:
    raise ValueError("Nessuna chiave 'binaccN' trovata nel JSON: controlla il contenuto.")

# 5) Estrai i valori
binacc = [data[f'binacc{n}'] for n in steps]
mae    = [data.get(f'mae{n}', None)   for n in steps]
rmse   = [data.get(f'rmse{n}', None)  for n in steps]

# Stampa diagnostica dei valori
print("Steps:", steps)
print("Binacc:", binacc)
print("MAE:", mae)
print("RMSE:", rmse)

# 6) Plotta
plt.figure(figsize=(10, 6))
plt.plot(steps, binacc, marker='o', label='Binacc (%)')
plt.plot(steps, mae,    marker='s', label='MAE')
plt.plot(steps, rmse,   marker='^', label='RMSE')

plt.title('Andamento di Binacc, MAE e RMSE per step')
plt.xlabel('Step')
plt.ylabel('Valore')
plt.xticks(steps)
plt.legend()
plt.grid(True)

# 7) Salva e mostra
plt.tight_layout()
plt.savefig('metriche_per_step.png', dpi=300)
plt.show()
