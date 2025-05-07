import tensorflow as tf

# Verifica se TensorFlow è stato compilato con supporto GPU
print("TensorFlow version:", tf.__version__)
print("Is TensorFlow using GPU:", tf.test.is_built_with_cuda())

# Elencare i dispositivi disponibili
print("Available devices:")
devices = tf.config.list_physical_devices()
for device in devices:
    print(f" - {device}")

# Controllare specificamente le GPU disponibili
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"Number of GPUs available: {len(gpus)}")
    for gpu in gpus:
        print(f" - {gpu}")
else:
    print("No GPUs detected.")

# Verificare se TensorFlow utilizza la GPU per i calcoli
try:
    # Creare un tensore e eseguire un'operazione su di esso
    with tf.device('/GPU:0'):  # Prova a usare la prima GPU
        a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
        b = tf.matmul(a, a)  # Moltiplicazione di matrici
    print("TensorFlow is using the GPU.")
except RuntimeError as e:
    print("Error while trying to use GPU:", e)
