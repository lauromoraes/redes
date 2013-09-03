import logging
import socket
import threading
import SocketServer
import time
from recvall import *

logging.basicConfig( level = logging.DEBUG, format = "%(name)s: %(message)s", )

class MyTCPRequestHandler(SocketServer.BaseRequestHandler):

	def __init__(self, request, client_address, server):
		self.logger = logging.getLogger('MyTCPRequestHandler')
		self.logger.debug('__init__')
		SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
		return

	def setup(self):
		self.logger.debug('setup')
		return SocketServer.BaseRequestHandler.setup(self)

	def handle(self):
		self.logger.debug('handle')
		data = recvall(self.request, 2)
		#print(self.request.accept()[1])
		#current_thread = threading.currentThread()
		#resp = "%s, %s" % (current_thread.getName(), data)
		#self.logger.debug('Thread: %s | recv()->"%s"', current_thread.getName(), data)
		#self.logger.debug('Threads: %s' % str( [ t.getName() for t in threading.enumerate()] ) )
		sent = 0
		size = 1024*5
		while(sent < len(data)):
			if(sent+size <= len(data)):
				sent += self.request.send(data[sent:sent+size])
			else:
				sent += self.request.send(data[sent:])
			time.sleep(0.1)
		#self.request.sendall("data")
		self.request.shutdown(socket.SHUT_WR)
		self.request.close()
		#time.sleep(3)
		return

	def finish(self):
		self.logger.debug('finish')
		return SocketServer.BaseRequestHandler.finish(self)
