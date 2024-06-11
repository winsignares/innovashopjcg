# main.py or app.py (your main application file)
from flask import Flask, render_template, request, jsonify, redirect, session, make_response
from config.db import app, db  # Assuming this sets up your Flask app
from models.Administrador import Administrador
from controllers.hashing_helper import hash_password

from controllers.Auth import ruta_auth
from controllers.Administrador import ruta_admin
from controllers.Usuarios import ruta_user
from controllers.Indexes import ruta_index  
from controllers.Empresa import ruta_empresa
from controllers.Cliente import ruta_cliente
from controllers.Proveedor import ruta_proveedor
from controllers.Producto import ruta_productos
from controllers.Vendedores import ruta_vendedor

# Register blueprints
app.register_blueprint(ruta_auth, url_prefix="/auth")
app.register_blueprint(ruta_admin, url_prefix="/admin")
app.register_blueprint(ruta_user, url_prefix="/user")
app.register_blueprint(ruta_empresa, url_prefix="/empresa")
app.register_blueprint(ruta_cliente, url_prefix="/cliente")
app.register_blueprint(ruta_proveedor, url_prefix="/proveedor")  # Ensure this line is correct
app.register_blueprint(ruta_productos, url_prefix="/producto")
app.register_blueprint(ruta_vendedor, url_prefix="/vendedor")

app.register_blueprint(ruta_index, url_prefix="/")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def unauthorized_error(e):
    return render_template('403.html'), 403

def create_default_admin():
    default_admin_user = 'DabiAdmin'
    default_admin_name = 'Dabisito'
    default_admin_password = 'dabisito123'

    existing_admin = Administrador.query.filter_by(usuario=default_admin_user).first()
    if not existing_admin:
        hashed_password = hash_password(default_admin_password)
        new_admin = Administrador(
            nombre=default_admin_name,
            usuario=default_admin_user,
            contraseña=hashed_password
        )
        db.session.add(new_admin)
        db.session.commit()
        print("Default admin created.")

if __name__ == '__main__':
    with app.app_context():
        create_default_admin()
    app.run(debug=True)
