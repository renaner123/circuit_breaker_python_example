from math import log
import requests
import time
import logging

STATE_OPEN = "open"
STATE_CLOSED = "closed"
STATE_HALF_OPEN = "half-open"

logging.basicConfig(level=logging.INFO, format='INFO: %(message)s')

class CircuitOpenException(Exception):
    pass

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
        if self.state == STATE_OPEN:
            if (current_time - self.last_failure_time) > self.reset_timeout:
                self.state = STATE_HALF_OPEN
                logging.info("estado alterou de OPEN para HALF-OPEN")
            else:
                logging.info("Circuit is open")
                raise CircuitOpenException()

        elif self.state == STATE_HALF_OPEN:
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()  
                if response:
                    logging.info('Response: %s', response.json())
                    self.state = STATE_CLOSED
                    self.last_failure_time = current_time
                    self.fail_counter = 0
                    logging.info("estado alterou de HALF-OPEN para CLOSED")
                return response

            except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
                self.fail_counter += 1
                self.last_failure_time = current_time
                logging.info('Fail counter: %s', self.fail_counter)
                self.state = STATE_OPEN
                raise

        else:
            if(self.fail_counter >= self.fail_max):
                self.state = STATE_OPEN
                self.last_failure_time = current_time
                logging.info("estado alterou de CLOSED para OPEN")
            else:
                try:
                    response = func(*args, **kwargs)
                    response.raise_for_status() 
                    return response

                except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
                    self.fail_counter += 1
                    self.last_failure_time = current_time
                    logging.info('Fail counter: %s', self.fail_counter)
                    raise

def get_data(breaker, key, timeout=30):
    try:
        response = breaker.call(requests.get, f'http://127.0.0.1:5000/data/{key}', timeout=timeout)
        if response:
            logging.info('Response: %s', response.json())
            return response.json()
    except CircuitOpenException:
        return {"error": "Circuit is open"}
    except (requests.exceptions.RequestException, ValueError) :
        return {'error': 'Service Unavailable'}

def set_data(breaker, key, value, timeout=5):
    try:
        response = breaker.call(requests.post, f'http://127.0.0.1:5000/data/{key}', json={'value': value}, timeout=timeout)
        return response.json()
    except (requests.exceptions.RequestException, ValueError) :
        return {'error': 'Service Unavailable'}

if __name__ == '__main__':
    breaker = CircuitBreaker(fail_max=3, reset_timeout=10)

    set_data(breaker, 'testkey', 'testvalue')
    time.sleep(2)

    for _ in range(50):
        get_data(breaker, 'testkey')
        time.sleep(1)
