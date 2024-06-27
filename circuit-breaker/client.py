import requests
import time
import argparse
import logging
from circuit_breaker import CircuitBreaker, CircuitOpenException

logging.basicConfig(level=logging.INFO, format='INFO: %(message)s')

def get_data(breaker_call, key, timeout=30):
    try:
        response = breaker_call.call(requests.get, f'http://127.0.0.1:5000/data/{key}', timeout=timeout)
        if response:
            logging.info('Response: %s', response.json())
            return response.json()
    except CircuitOpenException:
        return {"error": "Circuit is open"}
    except (requests.exceptions.RequestException, ValueError):
        return {'error': 'Service Unavailable'}

def set_data(breaker_call, key, value, timeout=5):
    try:
        response = breaker_call.call(requests.post, f'http://127.0.0.1:5000/data/{key}', json={'value': value}, timeout=timeout)
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return {'error': 'Service Unavailable'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fail_max', type=int, default=3, help='Número máximo de falhas antes de abrir o circuito.')
    parser.add_argument('--reset_timeout', type=int, default=10, help='Tempo em segundos para aguardar antes de tentar reabrir o circuito.')
    parser.add_argument('--number_requests', type=int, default=50, help='Número de requisições para testar o circuito.')


    args = parser.parse_args()

    breaker = CircuitBreaker(args.fail_max, args.reset_timeout)

    set_data(breaker, 'testkey', 'testvalue')
    time.sleep(2)

    for _ in range(args.number_requests):
        get_data(breaker, 'testkey')
        time.sleep(1)
