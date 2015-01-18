class GamePlayer():
	def __init__(self, name, socket_id):
		self.name = name
		self.socket_id = socket_id

class GameServer():
	def __init__(self):
		self.players = {}

	def add_player(self, name, socket_id):
		player = GamePlayer(name, socket_id)
		self.play

	def accept_message(self, message):
		from interface import CommInterface

		print('The game server has received the command [%s]' % message)
		CommInterface.send_to_webserver('The game server has responded to the command.')