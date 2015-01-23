class CommPacket():
	def __init__(self, sent_by=None, send_to=None, message=None, server_command=None,
		server_args=None):
		self.sent_by = sent_by
		self.send_to = send_to
		self.message = message
		self.server_command = server_command
		self.server_args = server_args
