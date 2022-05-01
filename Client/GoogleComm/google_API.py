from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import json, os

app = Flask(__name__)


@app.route('/prime', methods=['POST'])
def prime():
    content = request.get_json() #JSON
    dir = "/home/pi/VCAvoidanceCar/Client/data"
    name = "request.json"
    path = os.path.join(dir, name)
    f = open(path, 'w')
    f.write(json.dumps(content))
    f.close()

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')