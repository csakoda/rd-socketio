class CommInterface():
	webserver = None
	gameserver = None

	def __init__(self):
		pass

	@classmethod
	def send_to_webserver(cls, message):
		cls.webserver.accept_message(message)

	@classmethod
	def send_to_gameserver(cls, message):
		cls.gameserver.accept_message(message)