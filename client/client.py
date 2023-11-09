import requests
import random
import time
import logging as log

log.basicConfig(level=log.INFO)

# URL de tu servidor Flask
server_url = 'http://servidor:5000'

def generate_random_username():
    # Genera un nombre de usuario aleatorio
    return 'user' + str(random.randint(1, 1000))

def send_request():
    # Envia una solicitud al servidor Flask con un nombre de usuario aleatorio
    username = generate_random_username()
    log.info("Registering User: %s", username)
    response = requests.post(f'{server_url}/formulario', data={'nombre': username})
    
    # Imprime la respuesta del servidor
    log.info("SUCCESFULLY REGISTERED User: %s", username)

if __name__ == '__main__':
    while True:
        # Envia solicitudes indefinidamente
        send_request()

        # Duerme un tiempo aleatorio entre 1 y 5 segundos
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)