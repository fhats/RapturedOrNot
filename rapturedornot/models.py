from google.appengine.ext import db

class Cultist(db.Model):
    fb_id = db.StringProperty(required = True)
    upvotes = db.IntegerProperty(required = True)
    voters = db.IntegerProperty(required = True)
