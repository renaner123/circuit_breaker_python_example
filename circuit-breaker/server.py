from flask import Flask, request, jsonify
import random

app = Flask(__name__)

class Server:

    def __init__(self) -> None:
        self.data_store = {}
        self.fail_chance = 0.5
        self.amount_fail = 2
        self.count_fail = 0

    def get_data(self, key):
        print("########", self.count_fail, self.amount_fail, self.fail_chance)
        if (random.random() < self.fail_chance) and (self.count_fail < self.amount_fail):
            self.count_fail += 1
            return "Service Unavailable", 503
        return jsonify({key: self.data_store.get(key, "Key not found")})

    def set_data(self, key):
        if random.random() < self.fail_chance:
            return "Service Unavailable", 503
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
