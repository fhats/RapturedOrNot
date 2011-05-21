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
    percentage = -1
    user = None
    if session.has_key('username'):
        user = Voter.all().filter("fb_id =", session['username']).get()
        votee = Votee.all().filter("fb_id =", session['username']).get()
        if votee is not None:
            percentage = float(votee.upvotes)/votee.voters*100.0
    return render_template('index.html', session=session, percentage=percentage, user=user)

    
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
    logging.info(request.form['friendJson'])
    friends = json.loads(request.form['friendJson'])['data']
    logging.info(str(friends))
    
    fb_id = request.form['fb_id']
    session['username'] = fb_id
    
    new_voter = Voter.all().filter("fb_id =", fb_id).get()
    if new_voter is None:
        new_voter = Voter(fb_id = session['username'],
                          friend_names = [x['name'] for x in friends],
                          friend_ids = [x['id'] for x in friends],
                          votes = [False for _ in friends])
        for f in friends:
            votee = Votee.all().filter("fb_id =", f['id']).get()
            if votee is None:
                new_votee = Votee(fb_id=f['id'], upvotes=0, voters=1)
                new_votee.put()
            else:
                votee.voters += 1
                votee.put()
    else:
        new_voter.friend_names = [x['name'] for x in friends]
        new_voter.friend_ids = [x['id'] for x in friends]
        if len(new_voter.votes) != len(new_voter.friend_names):
            votes = [False for _ in friends]
    db.put(new_voter)
    return redirect(url_for('index', ))

@app.route('/create2')
def create2():
    session['username'] = 'mud'
    
    new_voter = Voter.all().filter("fb_id =", session['username']).get()
    if new_voter is None:
        friends = [
            dict(name='Harold', id='1'),
            dict(name='Carol', id='2'),
            dict(name='Darrell', id='3'),
        ]
        new_voter = Voter(fb_id = session['username'],
                          friend_names = [x['name'] for x in friends],
                          friend_ids = [x['id'] for x in friends],
                          votes = [False for _ in friends])
        for f in friends:
            votee = Votee.all().filter("fb_id =", f['id']).get()
            if votee is None:
                new_votee = Votee(fb_id=f['id'], upvotes=0, voters=1)
                new_votee.put()
            else:
                votee.voters += 1
                votee.put()
        db.put(new_voter)
    return jsonify(status="ok", name="Lunchbox", id=920548)

@app.route('/show/<int:which_friend>')
def show(which_friend):
    if not session.has_key('username'): return redirect(url_for('index'))
    fb_id = session['username']
    voter = Voter.all().filter("fb_id =", fb_id).get()
    friend_name = voter.friend_names[which_friend]
    friend_fb_id = voter.friend_ids[which_friend]
    next_url = url_for('show', which_friend=which_friend+1) if (which_friend < len(voter.friend_names)-1) else None
    upvote_url = url_for('upvote', which_friend=which_friend)
    downvote_url = url_for('downvote', which_friend=which_friend)
    if voter is not None:
        return render_template('show.html', friend_name=friend_name, friend_fb_id=friend_fb_id, next_url=next_url, upvote_url=upvote_url, downvote_url = downvote_url)
    else:
        return redirect(url_for('index'))

@app.route('/list')
def list():
    if not session.has_key('username'): return redirect(url_for('index'))
    fb_id = session['username']
    voter = Voter.all().filter("fb_id =", fb_id).get()
    return render_template('all_votes.html', items = zip(voter.friend_names, voter.votes))

def vote(ix, val):
    if not session.has_key('username'): return redirect(url_for('index'))
    fb_id = session['username']
    voter = Voter.all().filter("fb_id =", fb_id).get()
    voter.votes[ix] = val
    voter.put()
    if ix < len(voter.friend_names)-1:
        return redirect(url_for('show', which_friend=ix+1))
    else:
        return redirect(url_for('list'))

@app.route('/upvote/<int:which_friend>')
def upvote(which_friend):
    return vote(which_friend, True)

@app.route('/downvote/<int:which_friend>')
def downvote(which_friend):
    return vote(which_friend, False)
    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
    
@app.route('/tos')
def tos():
    return render_template('tos.html')