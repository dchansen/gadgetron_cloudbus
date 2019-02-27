from flask import Flask, jsonify, request, abort
import datetime
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

workers = {}

timeout = datetime.timedelta(minutes=5)


@app.route('/cloudbus/add_worker', methods=['POST'])
def add_worker():
    global workers
    if not request.json and request.json['port']:
        abort(418)
    print(request.remote_addr)
    worker = '[' + request.remote_addr + ']:' + request.json['port']
    workers[worker] = {"last_heard_from": datetime.datetime.now()}
    return "OK"


@app.route('/cloudbus/workers', methods=['GET'])
def get_workers():
    global workers
    workers = {k: v for k, v in workers.items() if
               (datetime.datetime.now() - v["last_heard_from"]) < timeout}
    return jsonify(list(workers.keys()))


if __name__ == '__main__':
    # app.run(debug=True)
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
