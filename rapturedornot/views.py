from rapturedornot import app
from models import *

from flask import render_template, flash, url_for, redirect
from flaskext import wtf
from flaskext.wtf import validators

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/loginplz')
def loginplz():
    return render_template('loginplz.html')
