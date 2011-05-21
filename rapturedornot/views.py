import simplejson as json

from rapturedornot import app
from models import *

from flask import render_template, flash, url_for, redirect, session
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.ext import db

@app.route('/')
def index():
    return render_template('base.html', session=session)

@app.route('/loginplz')
def loginplz():
    return render_template('loginplz.html')

@app.route('/create', methods=['POST'])
def create():
    session['username'] = session.get('fb_id')
    session['fb_auth'] = session.get('fb_auth')
    new_voter = db.get(session.get('fb_id'))
    if new_voter is None:
        friends = json.loads(session.get('friends'))
        new_voter = Voter(fb_id = session.get('fb_id'),
                          friends = friends,
                          votes = [False for _ in friends])
        db.put(new_voter)
    return redirect(url_for('show', fb_id, 0))

@app.route('/show/<fb_id>/<int:which_friend>')
def show(fb_id, which_friend):
    return render_template('base.html')
