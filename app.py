from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__, 
            static_folder='config/static',
            template_folder='config/templates')

from controllers.empresa import ruta_empresa
from controllers.productos import productos_bp
from controllers.vendedor import ruta_vendedor
from controllers.proveedores import ruta_proveedores
from controllers.cliente import ruta_clientes
from controllers.users import ruta_user

app.register_blueprint(ruta_user, url_prefix="/controller")
app.register_blueprint(productos_bp, url_prefix="/controller")
app.register_blueprint(ruta_empresa, url_prefix="/controller")
app.register_blueprint(ruta_proveedores, url_prefix="/controller")
app.register_blueprint(ruta_vendedor, url_prefix="/controller")
app.register_blueprint(ruta_clientes, url_prefix="/controller")

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
