import inputs
from threading import Thread, Lock
import events
import socket, select
import sys

mutex = Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(2)

def send_data(device_id, device):
    for elem in device:
        for event in elem:
            key = (device_id, event.code, event.state)
            if key in events.EVENTS.keys():
                mutex.acquire()
                try:
                    print(events.EVENTS[key])
                    s.send(events.EVENTS[key].encode('utf-8'))
                except Exeption as e:
                    pass
                finally:
                    mutex.release()

if __name__ == "__main__":
    
    if(len(sys.argv) < 3) :
        print('Usage : python controllers.py hostname port')
        sys.exit()
       
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. Start sending messages')    
        
    for device_id, device in enumerate(inputs.devices.gamepads):
        t = Thread(target = send_data, args = ( device_id, device ) )
        t.start()
