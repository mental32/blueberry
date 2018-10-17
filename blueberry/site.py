import flask

public = flask.Blueprint(__name__, 'index')
private = flask.Blueprint(__name__ + '_api', 'api', url_prefix='/api/v1')

@public.route('/')
@public.route('/index')
def index():
	return flask.render_template('index.html')

@private.route('/ping')
def pong():
	return 'OK'
