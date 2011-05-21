import time

from flask import Flask
import settings

app = Flask('rapturedornot')
app.config.from_object('rapturedornot.settings')

@app.context_processor
def inject_stupid():
    return dict(stupidtime=str(time.time()))

import views
