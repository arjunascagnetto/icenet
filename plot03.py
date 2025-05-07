import json
import math
import matplotlib.pyplot as plt

# 1) Carica il JSON da file
with open('results/networks/tutorial_testrun/tutorial_testrun_42_history.json', 'r') as f:
    data = json.load(f)

# 2) Prepara i dati:
#    - Per ogni metrica (p. es. "loss", "binacc", ...) i suoi valori ordinati per indice
series = {}
for metric, values in data.items():
    # values è un dict con chiavi "0", "1", ..., "49"
    # ordiniamo per indice e ne estraiamo la lista
    idx = sorted(int(k) for k in values.keys())
    series[metric] = [values[str(i)] for i in idx]

# 3) Calcola layout subplots
metrics = list(series.keys())
n = len(metrics)
cols = 4
rows = math.ceil(n / cols)

# 4) Crea la figura e i subplot
fig, axes = plt.subplots(rows, cols, figsize=(16, rows*3), sharex=True)
axes = axes.flatten()

# 5) Disegna ogni serie nel proprio subplot
for ax, metric in zip(axes, metrics):
    y = series[metric]
    x = list(range(len(y)))
    ax.plot(x, y, marker='o', linestyle='-')
    ax.set_title(metric, pad=10)
    ax.set_xlabel('Epoch')
    ax.set_ylabel(metric)
    ax.grid(True)

# 6) Nascondi eventuali subplot vuoti
for ax in axes[n:]:
    ax.axis('off')

# 7) Rifinisci layout e salva
plt.tight_layout()
plt.savefig('tutte_le_metriche.png', dpi=300)
plt.show()
