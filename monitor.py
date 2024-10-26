# monitor.py
import time
import subprocess


def start_app():
    # Inicia la aplicación principal
    print("Iniciando main.py...")
    subprocess.Popen(['python', 'main.py'])


def is_running():
    # Verifica si la aplicación principal está en ejecución
    try:
        result = subprocess.check_output(
            ['pgrep', '-f',
             'main.py'])  # Busca procesos con el nombre 'main.py'
        return len(result) > 0
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    # Ejecuta un ciclo de monitoreo
    while True:
        if not is_running():
            print("La aplicación no está en ejecución. Reiniciando...")
            start_app()
        time.sleep(10)  # Espera 10 segundos antes de verificar nuevamente
