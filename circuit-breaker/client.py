import requests
import time
import logging

STATE_OPEN = "open"
STATE_CLOSED = "closed"
STATE_HALF_OPEN = "half-open"

logging.basicConfig(level=logging.INFO, format='INFO: %(message)s')

class CircuitBreaker:

    def __init__(self, fail_max, reset_timeout) -> None:
        logging.info('Circuit Breaker initialized')
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_counter = 0
        self.state = STATE_CLOSED
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        current_time = time.time()
        logging.info('Fail counter: %s', self.fail_counter)

        if self.state == STATE_OPEN:
            logging.info('Circuit is OPEN')
            if (current_time - self.last_failure_time) > self.reset_timeout:
                self.state = STATE_HALF_OPEN
            else:
                raise Exception("Circuit is OPEN")

        elif self.state == STATE_HALF_OPEN:
            logging.info('Circuit is HALF_OPEN')
            self.state = STATE_CLOSED
            self.fail_counter = 0

        else:
            try:
                logging.info('STATE_CLOSED')
                response = func(*args, **kwargs)
                response.raise_for_status()  # Ensure we handle HTTP errors
                return response

            except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
                self.fail_counter += 1
                self.last_failure_time = current_time
                raise

def get_data(breaker, key, timeout=30):
    try:
        response = breaker.call(requests.get, f'http://127.0.0.1:5000/data/{key}', timeout=timeout)
        return response.json()
    except requests.exceptions.RequestException:
        return 'Service Unavailable'
    except ValueError:
        return 'Service Unavailable'

def set_data(breaker, key, value, timeout=5):
    try:
        response = breaker.call(requests.post, f'http://127.0.0.1:5000/data/{key}', json={'value': value}, timeout=timeout)
        return response.json()
    except requests.exceptions.RequestException:
        return 'Service Unavailable'
    except ValueError:
        return 'Service Unavailable'

if __name__ == '__main__':
    breaker = CircuitBreaker(fail_max=3, reset_timeout=5)

    print(set_data(breaker, 'testkey', 'testvalue'))

    for _ in range(10):
        print('Recebido do servidor:', get_data(breaker, 'testkey'))
        time.sleep(2)
