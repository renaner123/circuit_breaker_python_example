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

    def __init__(self, threshold, reset_timeout) -> None:
        logging.info('Circuit Breaker initialized')
        self.threshold = threshold
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

            except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                logging.error(e)
                self.fail_counter += 1
                self.last_failure_time = current_time
                self.state = STATE_OPEN
                logging.info("estado alterou de HALF-OPEN para OPEN")  
                raise

        else:
            if(self.fail_counter >= self.threshold):
                self.state = STATE_OPEN
                self.last_failure_time = current_time
                logging.info("estado alterou de CLOSED para OPEN")
            else:
                try:
                    response = func(*args, **kwargs)
                    response.raise_for_status() 
                    return response

                except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                    self.fail_counter += 1
                    self.last_failure_time = current_time
                    logging.error(e)
                    #logging.info('Fail counter: %s', self.fail_counter)
                    raise
