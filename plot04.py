import json
import os
import matplotlib.pyplot as plt

# 1) Carica il JSON da file
json_path = 'results/networks/api_test_run/api_test_run_42_history.json'
if not os.path.exists(json_path):
    raise FileNotFoundError(f"File '{json_path}' non trovato.")

with open(json_path, 'r') as f:
    data = json.load(f)

# 2) Definisci le metriche che vuoi plottare
train_metrics = ['loss', 'binacc', 'mae', 'rmse', 'mse']
val_metrics   = ['val_loss', 'val_binacc', 'val_mae', 'val_rmse', 'val_mse']

# 3) Estrai le serie ordinate per epoca
def extract_series(name):
    vals = data.get(name, {})
    # ordina le chiavi numeriche e ritorna la lista di valori
    indices = sorted(int(k) for k in vals.keys())
    return [vals[str(i)] for i in indices]

# 4) Crea figura e subplot
fig, axes = plt.subplots(2, 5, figsize=(20, 8), sharex=True)
epochs = None

# riga training
for col, metric in enumerate(train_metrics):
    series = extract_series(metric)
    if epochs is None:
        epochs = list(range(len(series)))
    ax = axes[0, col]
    ax.plot(epochs, series, marker='o', linewidth=1)
    ax.set_title(metric)
    ax.set_ylabel(metric)
    ax.grid(True)

# riga validation
for col, metric in enumerate(val_metrics):
    series = extract_series(metric)
    ax = axes[1, col]
    ax.plot(epochs, series, marker='o', linewidth=1)
    ax.set_title(metric)
    ax.set_xlabel('Epoch')
    ax.set_ylabel(metric)
    ax.grid(True)

# 5) Rifinisci e salva
plt.tight_layout()
plt.savefig('images/metriche_training_vs_validation2.png', dpi=300)
plt.show()
