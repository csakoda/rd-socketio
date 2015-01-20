class CommInterface():
	webserver = None
	gameserver = None

	def __init__(self):
		pass

	@classmethod
	def send_to_webserver(cls, message):
		if message.__class__ is CommPacket:
			cls.webserver.accept_message(message)
		else:
			print('Interface received a message not of type CommPacket')

	@classmethod
	def send_to_gameserver(cls, message):
		if message.__class__ is CommPacket:
			cls.gameserver.accept_message(message)
		else:
			print('Interface received a message not of type CommPacket')

class CommPacket():
	def __init__(self, sent_by=None, send_to=None, message=None, server_command=None,
		server_args=None):
		self.sent_by = sent_by
		self.send_to = send_to
		self.message = message
		self.server_command = server_command
		self.server_args = server_args