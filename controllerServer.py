# Tcp Chat server

import socket, select
import pyautogui

BUTTON_MAP = {
	"0XL": "1", 
	"0YD": "2",
	"0A": "3",
	"0B": "4",
	"0C": "5",
	"0D": "6",
	"0E": "7",
	"0F": "8",
	"0XR": "9",
	"0YD": "0",

	"1XL": "q", 
	"1YD": "w",
	"1A": "e",
	"1B": "r",
	"1C": "t",
	"1D": "y",
	"1E": "u",
	"1F": "i",
	"1XR": "o",
	"1YU": "p", 

	"2XL": "a", 
	"2YD": "s",
	"2A": "d",
	"2B": "f",
	"2C": "g",
	"2D": "h",
	"2E": "j",
	"2F": "k",
	"2XR": "l",
	"2YU": ";",

	"3XL": "z", 
	"3YD": "x",
	"3A": "c",
	"3B": "v",
	"3C": "b",
	"3D": "n",
	"3E": "m",
	"3F": ",",
	"3XR": ".",
	"3YU": "/",
}

axes = ("0X", "0Y",
		"1X", "1Y",
		"2X", "2Y",
		"3X", "3Y")

last_turns = {
	"0": None,
	"1": None,
	"2": None,
	"3": None
}

def transform_data_to_keypress (sock, message):
	button = message[0:2]
	action = message[2]
	if button in axes and action != "C":
		pyautogui.keyDown(BUTTON_MAP[message[0:3])
		last_turns[button[0]] == BUTTON_MAP[message[0:3]]
	else if button in axes and action == "C":
		pyautogui.keyUp(last_turns[button[0]])
	else:
		if action == "U":
			pyautogui.keyUp(BUTTON_MAP[button])
		else if action == "D":
			pyautogui.keyDown(BUTTON_MAP[button])
		else:
			print("error!")	

if __name__ == "__main__":
	
	# List to keep track of socket descriptors
	CONNECTION_LIST = []
	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	PORT = 5000
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# this has no effect, why ?
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)

	# Add server socket to the list of readable connections
	CONNECTION_LIST.append(server_socket)

	print "Chat server started on port " + str(PORT)

	while 1:
		# Get the list sockets which are ready to be read through select
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

		for sock in read_sockets:
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr
			
			#Some incoming message from a client
			else:
				# Data recieved from client, process it
				try:
					#In Windows, sometimes when a TCP program closes abruptly,
					# a "Connection reset by peer" exception will be thrown
					data = sock.recv(RECV_BUFFER)
					if data:
						transform_data_to_keypress(sock, data)                
				
				except:
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	
	server_socket.close()
