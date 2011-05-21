from flask import Flask
import settings

app = Flask('rapturedornot')
app.config.from_object('rapturedornot.settings')

import views
