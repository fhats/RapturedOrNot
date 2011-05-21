from google.appengine.ext import db

class Voter(db.Model):
    fb_id = db.StringProperty(required = True)
    friend_ids = db.StringListProperty(required = True)
    friend_names = db.StringListProperty(required = True)
    votes = db.ListProperty(bool, required = True)

class Votee(db.Model):
    fb_id = db.StringProperty(required = True)
    upvotes = db.IntegerProperty(required = True)
    voters = db.IntegerProperty(required = True)
