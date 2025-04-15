import time
import subprocess
import threading

class NvidiaSmiMeasure:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        print("###################Debut de la mesure nvidia-smi###########################")
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        print("###################Fin de la mesure nvidia-smi###########################")
        if self.thread is not None:
            self.thread.join()

    def run(self):
        with open("consommation_energie_gpu.csv", "w") as f:
            f.write("timestamp,gpu_power\n")
            start_time = time.time()  # Temps de départ
            elapsed_time = 0  # Temps écoulé initialisé à 0

            try:
                while self.running:
                    # Exécuter la commande nvidia-smi pour obtenir la consommation d'énergie
                    result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], capture_output=True, text=True)
                    gpu_power = result.stdout.strip().split('\n')[0]  # Prendre la première ligne de la sortie
                    f.write(f"{elapsed_time},{gpu_power}\n")
                    time.sleep(0.1)
                    f.flush()  # Forcer l'écriture immédiate sur le disque
                    elapsed_time = time.time() - start_time  # Mettre à jour le temps écoulé
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    measure = NvidiaSmiMeasure()
    measure.start()
    try:
        # Laisser le script tourner pendant 10 secondes à titre d'exemple
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        measure.stop()
