from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import json

app = Flask(__name__)


@app.route('/prime', methods=['POST'])
def prime():
    content = request.get_json() #JSON
    content['valid'] = True
    f = open("request.txt", 'w')
    f.write(json.dumps(content))
    f.close()

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')
