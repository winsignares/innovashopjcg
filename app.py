from flask import Flask, request, jsonify
from config.common.token import* 
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hola mundo"

@app.route('/obtenertoken', methods=['GET'])
def obtenertoken():
    datatoken = generar_token("Gatcia", 963)
    var_token = datatoken['token']
    response = {
      "statusCode": 200,
      "body": json.dumps(var_token)
    }
    return jsonify(response)



if __name__ == "__main__":
    app.run(debug=True)
