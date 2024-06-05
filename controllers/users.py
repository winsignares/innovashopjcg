import controllers.users
from flask import Flask, jsonify, request, redirect, session, make_response, Blueprint, render_template, url_for, flash
from models.Admin import Admin, AdminSchema
from config.db import app, db, ma
from datetime import datetime, timedelta, timezone
import jwt

ruta_user = Blueprint("route_user", __name__)

admin_shchema = AdminSchema()
admins_shchema = AdminSchema(many=True)

SECRET_KEY = "newtoken"

def generar_token_admin(user_id):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=150)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


@app.route('/admins', methods=['GET'])
def admins():
    return render_template('admin.html')
    
@app.route('/login_v')
def login_view():
    return render_template('login.html')