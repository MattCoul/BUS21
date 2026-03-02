from flask import render_template, redirect, url_for, flash, request
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
