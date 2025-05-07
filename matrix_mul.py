import tensorflow as tf
import time

# Dimensione delle matrici
MATRIX_SIZE = 10000

# Funzione per misurare il tempo di esecuzione della moltiplicazione su CPU
def matrix_multiplication_cpu():
    print("Eseguo la moltiplicazione su CPU...")
    with tf.device('/CPU:0'):  # Forza l'esecuzione sulla CPU
        a = tf.random.uniform((MATRIX_SIZE, MATRIX_SIZE))
        b = tf.random.uniform((MATRIX_SIZE, MATRIX_SIZE))
        
        start_time = time.time()
        result = tf.matmul(a, b)  # Moltiplicazione delle matrici
        _ = result.numpy()  # Forza l'esecuzione dell'operazione (calcolo eager)
        end_time = time.time()
    
    print(f"Tempo di esecuzione su CPU: {end_time - start_time:.4f} secondi")

# Funzione per misurare il tempo di esecuzione della moltiplicazione su GPU
def matrix_multiplication_gpu():
    if not tf.config.list_physical_devices('GPU'):
        print("Nessuna GPU disponibile. Saltata l'esecuzione su GPU.")
        return
    
    print("Eseguo la moltiplicazione su GPU...")
    with tf.device('/GPU:0'):  # Forza l'esecuzione sulla GPU
        a = tf.random.uniform((MATRIX_SIZE, MATRIX_SIZE))
        b = tf.random.uniform((MATRIX_SIZE, MATRIX_SIZE))
        
        start_time = time.time()
        result = tf.matmul(a, b)  # Moltiplicazione delle matrici
        _ = result.numpy()  # Forza l'esecuzione dell'operazione (calcolo eager)
        end_time = time.time()
    
    print(f"Tempo di esecuzione su GPU: {end_time - start_time:.4f} secondi")

# Verifica se TensorFlow rileva una GPU
print("Verifica dispositivi disponibili:")
print(tf.config.list_physical_devices())

# Esegui le moltiplicazioni
matrix_multiplication_cpu()
matrix_multiplication_gpu()
