import logging
import socket
import threading
import SocketServer

logging.basicConfig( level = logging.DEBUG, format = "%(name)s: %(message)s", )

class UDPHandler( SocketServer.UDPServer ):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		print( "{} wrote:".format( self.client_address[0] ) )
		print( data )
		socket.sendoto( data.upper(), self.client_address )
