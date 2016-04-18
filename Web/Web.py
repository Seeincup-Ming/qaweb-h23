# -*- coding: utf-8 -*-
import os
from flask import Flask
app = Flask(__name__)

app.secret_key = 'some_secret'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max 16M
app.config['DEBUG'] = bool(os.getenv('DEBUG'))

def register_routers():
    from routers import home,svnlock#, api
    app.register_blueprint(home.bp, url_prefix='')
    app.register_blueprint(svnlock.bp, url_prefix='/svnlock')
    #app.register_blueprint(api.bp, url_prefix='/api')

port = os.getenv('PORT') or '8000'
if __name__ == '__main__':
    register_routers()
    app.run(debug=True, host='0.0.0.0', port=int(port))




