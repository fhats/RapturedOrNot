import simplejson as json

import logging

from rapturedornot import app
from models import *

from flask import render_template, flash, jsonify, url_for, redirect, session
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.ext import db

@app.route('/')
def index():
    return render_template('index.html', session=session)

    
@app.route('/login', methods=['POST'])
def login():
    session['username'] = session.get('fb_id')
    new_voter = db.get(session.get('fb_id'))
    
    logging.info("HEY BUDDY: %s", session['username'])
    
    if new_voter is None:
        return jsonify(status="error", need="friends")
    else:
        return jsonify(status="ok")

@app.route('/create', methods=['POST'])
def create():
    session['username'] = session.get('fb_id')
    new_voter = db.get(session.get('fb_id'))
    if new_voter is None:
        friends = json.loads(session.get('friends'))
        new_voter = Voter(fb_id = session.get('fb_id'),
                          friends = friends,
                          votes = [False for _ in friends])
        db.put(new_voter)
    return redirect(url_for('index', ))

@app.route('/show/<fb_id>/<int:which_friend>')
def show(fb_id, which_friend):
    return render_template('index.html')

    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
    
@app.route('/tos')
def tos():
    return render_template('tos.html')