class GamePlayer():
	_registry = []

	def __init__(self, name, pid):
		self.name = name
		self.pid = pid
		GamePlayer._registry.append(self)
		print(p for p in GamePlayer._registry)

	@classmethod
	def get(cls, pid):
		for p in cls._registry:
			if p.pid == pid:
				return p
		else:
			print('not found')
			return None

class GameServer():
	def __init__(self):
		pass

	def accept_message(self, packet):

		print('The game server has received the command [%s] from [%s]' % 
			(packet.message, packet.sent_by))

		self.parse_packet(packet)

	def parse_packet(self, packet):
		from interface import CommInterface, CommPacket

		player_id = packet.sent_by
		message = packet.message

		if packet.server_command is 'login':
			print(packet.server_command)
			player_name = packet.server_args['name']
			player = GamePlayer(player_name, player_id)
			return

		player = GamePlayer.get(player_id)

		if player is None:
			response = CommPacket(send_to=[packet.sent_by,], 
				message='Socket [%i] has no player attached.' % player_id)
			CommInterface.send_to_webserver(response)
			return

		print(player, message)
		self.parse_message(player, message)

	def parse_message(self, player, message):
		command = message.split()[0]
		args = message.split()[1:]

		self.parse_command(player, command, args)

	def parse_command(self, player, command, args):
		from interface import CommInterface, CommPacket
		# Say only, for now
		if command == 'say':
			message = " ".join(args)
			self_response = CommPacket(send_to=[player.pid,], 
				message='You say \'%s\'' % message)
			room_response = CommPacket(
				send_to=[p.pid for p in GamePlayer._registry if p is not player],
				message='%s says \'%s\'' % (player.name, message))
			CommInterface.send_to_webserver(room_response)
			CommInterface.send_to_webserver(self_response)
		else:
			self_response = CommPacket(send_to=[player.pid,], 
				message='Huh? The only valid command is \'say\'.')
			CommInterface.send_to_webserver(self_response)
