import os

import flask

import blueberry

public = flask.Blueprint(__name__, 'index')
private = flask.Blueprint(__name__ + '_api', 'api', url_prefix='/api/v1')


@public.route('/')
@public.route('/index')
def index():
    return flask.render_template('index.html', app=blueberry._blueberries[os.getpid()])


@private.route('/ping')
def pong():
    return 'OK'
