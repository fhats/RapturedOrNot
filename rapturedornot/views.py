import simplejson as json

import logging

from rapturedornot import app
from models import *

from flask import request, render_template, flash, jsonify, url_for, redirect, session
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.ext import db

@app.route('/')
def index():
    return render_template('index.html', session=session)

    
@app.route('/login', methods=['POST'])
def login():
    fb_id = request.form['fb_id']
    session['username'] = fb_id
    
    new_voter = Voter.all().filter("fb_id =", fb_id).get()
    
    if new_voter is None:
        # JS sends us over to create()
        return jsonify(status="error", needs="friends")
    else:
        return jsonify(status="ok")

@app.route('/create', methods=['POST'])
def create():
    logging.info(request.form['friends'])
    
    fb_id = request.form['fb_id']
    session['username'] = fb_id
    
    new_voter = Voter.all().filter("fb_id =", fb_id).get()
    if new_voter is None:
        friends = json.loads(request.form['friends'])
        new_voter = Voter(fb_id = request.form['fb_id'],
                          friend_names = [x['name'] for x in friends],
                          friend_ids = [x['id'] for x in friends],
                          votes = [False for _ in friends])
        db.put(new_voter)
    return redirect(url_for('index', ))

@app.route('/show/<int:which_friend>')
def show(which_friend):
    return render_template('show.html')

@app.route('/upvote/<int:which_friend>')
def upvote(which_friend):
    return redirect(url_for('show', which_friend=0))

@app.route('/downvote/<int:which_friend>')
def downvote(which_friend):
    return redirect(url_for('show', which_friend=0))
    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
    
@app.route('/tos')
def tos():
    return render_template('tos.html')