import time
import subprocess
import threading
import argparse
import os
import signal

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
        pid = os.getpid()
        with open("/tmp/nv_measure.pid", "w") as f_pid:
            f_pid.write(str(pid))

        with open("/tmp/scratch/save_data/consommation_energie_gpu.csv", "w") as f:
            f.write("timestamp,gpu_power\n")
            start_time = time.time()
            elapsed_time = 0

            try:
                while self.running:
                    result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], capture_output=True, text=True)
                    gpu_power = result.stdout.strip().split('\n')[0]
                    f.write(f"{elapsed_time},{gpu_power}\n")
                    time.sleep(0.01)
                    f.flush()
                    elapsed_time = time.time() - start_time
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")
            finally:
                if os.path.exists("/tmp/nv_measure.pid"):
                    os.remove("/tmp/nv_measure.pid")

def main():
    parser = argparse.ArgumentParser(description='Mesurer la consommation d\'énergie GPU.')
    parser.add_argument('command', choices=['start', 'stop'], help='Commande pour démarrer ou arrêter la mesure.')

    args = parser.parse_args()

    measure = NvidiaSmiMeasure()

    if args.command == 'start':
        measure.start()
    elif args.command == 'stop':
        measure.stop()

if __name__ == "__main__":
    main()
