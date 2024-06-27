from flask import Flask, request, jsonify
import random
import argparse

app = Flask(__name__)

class Server:

    def __init__(self, fail_chance=1) -> None:
        self.data_store = {}
        self.fail_chance = fail_chance

    def get_data(self, key):
        if (random.random() < self.fail_chance):
            return "Service Unavailable", 503
        else:
            return jsonify({key: self.data_store.get(key, "Key not found")})

    def set_data(self, key):
        value = request.json.get('value')
        self.data_store[key] = value
        return jsonify({key: value})

parser = argparse.ArgumentParser()
parser.add_argument('--fail_chance', type=float, default=1, help='Change de falhas para o serviço retornar mensagem correta (0.0-1.0). 1 = 100% de falha. 0 = 0% de falha.')
args = parser.parse_args()

server = Server(fail_chance=args.fail_chance)

@app.route('/data/<key>', methods=['GET'])
def get_data_route(key):
    return server.get_data(key)

@app.route('/data/<key>', methods=['POST'])
def set_data_route(key):
    return server.set_data(key)

if __name__ == '__main__':
    app.run(debug=True)
