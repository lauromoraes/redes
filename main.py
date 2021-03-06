class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.error, msg:
			raise Usage(msg)
	except Usage, err:
		print >>sys.stderr, err.msg
		print >>sys.stderr, "for help use --help"
		return 2
	tcp, udp, server, client = "tcp", "udp", "server", "client"
	if len(argv) == 3:
		if udp in argv:
			if server in argv:
				print( "Init {protocol} {host_type}".format( protocol=udp, host_type=server ) )
			elif client in argv:
				print( "Init {protocol} {host_type}".format( protocol=udp, host_type=client ) )
			else:
				print("ERROR: Invalid parameters! ({opt1} | {opt2})".format( opt1=server, opt2=client ) )
				sys.exit(2)
		elif tcp in argv:
			if server in argv:
				try:
					from MyTCPServer import MyTCPServer
					msg = "Init {protocol} {host_type}".format(protocol=tcp, host_type=server)
					print(msg)
				except Exception as e:
					print >>sys.stderr, e
					sys.exit(2) 
			elif client in argv:
				try:
					from MyTCPClient import MyTCPClient
					msg = "Init {protocol} {host_type}".format(protocol=tcp, host_type=client)
					print(msg)
				except Exception as e:
					print >>sys.stderr, e
					sys.exit(2)
			else:
				print("ERROR: Invalid parameters! ({opt1} | {opt2})".format( opt1=server, opt2=client ) )
				sys.exit(2)
		else:
			print("ERROR: Invalid parameters! ({opt1} | {opt2})".format( opt1=tcp, opt2=udp ) )
			sys.exit(2)
	else:
		error = "ERROR: Parameters not found! Usage: main.py ({opt1}|{opt2}) ({opt3}|{opt4})".format( opt1=tcp, opt2=udp, opt3=server, opt4=client )
		print >>sys.stderr, error
		sys.exit(2)
'''
if __name__ == "__main__":
	import sys
	import getopt
	from RequestHandler import RequestHandler
	from MyUDPServer import MyUDPServer
	sys.exit(main())
'''

import sys
import getopt
from MyTCPRequestHandler import MyTCPRequestHandler
from MyTCPServer import MyTCPServer
if __name__ == '__main__':
    import socket
    import threading
    import logging
    logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)

    address = ('localhost', 0) # let the kernel give us a port
    server = MyTCPServer(address, MyTCPRequestHandler)
    ip, port = server.server_address # find out what port we were given

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message = 'Hello World!'
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')
    server.socket.close()
