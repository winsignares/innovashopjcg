from flask import Blueprint, render_template, request, redirect, session
from config.db import app, db, ma
from models.User import User, user_schema, users_schema
from models.Empresa import Empresa, EmpresaSchema
from controllers.user import user_schema

ruta_administrador = Blueprint('route_administrador', __name__)

@app.route('/admins', methods=['GET'])
def portaladministrativo():
    
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin.html',usuario = session['adminu'],  empresas=empresas)


@app.route('/reg_empresa')
def crearempresa():
    return render_template('admin-add-empresas.html')

@app.route('/search_by')
def search():
    query = request.args.get('query', '')

    if query:
        empresas = Empresa.query.filter(
            (Empresa.id.like(f'%{query}%')) |
            (Empresa.nombre.like(f'%{query}%'))
        ).all()
    else:
        empresas = Empresa.query.all()

    if 'adminu' in session:
        return render_template('admin-empresas.html', usuario=session['adminu'], empresas=empresas)