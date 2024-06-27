from flask import Flask, request, jsonify
import random

app = Flask(__name__)

class Server:

    def __init__(self) -> None:
        self.data_store = {}
        self.fail_chance = 0.3

    def get_data(self, key):
        if (random.random() < self.fail_chance):
            return "Service Unavailable", 503
        else:
            return jsonify({key: self.data_store.get(key, "Key not found")})

    def set_data(self, key):
        value = request.json.get('value')
        self.data_store[key] = value
        return jsonify({key: value})

server = Server()

@app.route('/data/<key>', methods=['GET'])
def get_data_route(key):
    return server.get_data(key)

@app.route('/data/<key>', methods=['POST'])
def set_data_route(key):
    return server.set_data(key)

if __name__ == '__main__':
    app.run(debug=True)
