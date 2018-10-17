
class Child:
	def __init__(self, ws, data):
		self._ws = ws
		self._data = data

	@property
	def ws(self):
		return self._ws

	@property
	def data(self):
		return self._data	

	def send(self, *args, **kwargs):
		return self._ws.send(*args, **kwargs)

	def recv(self, *args, **kwargs):
		return self._ws.recv(*args, **kwargs)
