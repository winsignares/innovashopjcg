from flask import Flask, request, jsonify
from config.common.token import * 
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



@app.route('/verificartoken', methods=['GET'])
def verificartoken():
    token = request.headers['Authorization']
    token = token.replace("Bearer", "")
    token = token.replace(" ", "")
    vf = verificar_token(token)
    return jsonify(vf)





if __name__ == "__main__":
    app.run(debug=True)
