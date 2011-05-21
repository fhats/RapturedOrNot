from google.appengine.ext import db

class Voter(db.Model):
    fb_id = db.StringProperty(required = True)
    friends = db.StringListProperty(required = True)
    votes = db.ListProperty(bool, required = True)
    
    def __init__(self, fb_id, *args, **kwargs):
        super(Voter, self).__init__( key_name=fb_id, fb_id=fb_id, **kwargs)

class Cultist(db.Model):
    fb_id = db.StringProperty(required = True)
    upvotes = db.IntegerProperty(required = True)
    voters = db.IntegerProperty(required = True)
    
    def __init__(self, fb_id, *args, **kwargs):
        super(Cultist, self).__init__(key_name=fb_id, fb_id=fb_id, **kwargs)
