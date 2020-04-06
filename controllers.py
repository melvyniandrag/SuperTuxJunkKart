"""
process for cancellation
if the button down is in the queue or l/r is in the queue, do not send again.
wait for a clearing signal, then send again.


opposite of mnD is mnU
opposite of mnL or mnR is mnC

if mnD is in SENT, do not send again until sending mnU
if mnL is in SENT, do not send again until sending mnC
if mnR is in SENT, do not send again until sending mnC
"""

import queue
import inputs
from threading import Thread, Lock
import events
import socket, select
import sys
import time

mutex = Lock()

q = queue.Queue()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(20)

already_sent_left_right = {
    0 : False,
    1 : False,
    2 : False,
    3 : False
}

already_sent_up_down = {
    0 : False,
    1 : False,
    2 : False,
    3 : False
}

sent = set()

def shouldBeSent(s):
    if s[2] in ["R", "L"]:
        if s in sent:
            return False
        else:
            sent.add(s)
            s_inverse = s[0:2] + "C"
            sent.discard(s_inverse)
            return True
    elif s[2] in ["C"]:
        if s in sent:
            return False
        else:
            sent.add(s)
            s_inverse1 = s[0:2] + "L"
            s_inverse2 = s[0:2] + "R"
            sent.discard(s_inverse1)
            sent.discard(s_inverse2)
            return True
    elif s[2] in ["D"]:
        if s in sent:
            return False
        else:
            sent.add(s)
            s_inverse = s[0:2] + "U"
            sent.discard(s_inverse)
            return True
    elif s[2] in ["U"]:
        if s in sent:
            return False
        else:
            sent.add(s)
            s_inverse = s[0:2] + "D"
            sent.discard(s_inverse)
            return True
    else:
        print("ERROR! Unexpected key to press! : " + s )
        return False;

def send_data(device_id, device):
    for elem in device:
        for event in elem:
            key = (device_id, event.code, event.state)
            if key in events.EVENTS.keys():
                strToSend = events.EVENTS[key]
                if not shouldBeSent(strToSend):
                    continue
                while 1:
                    if not mutex.locked():
                        mutex.acquire()
                        break;
                    else:
                        time.sleep(0.005)
                try:
                    q.put(strToSend.encode('utf-8'))
                except Exception as e:
                    print(str(e))
                    print("unable to send" + events.EVENTS[key]) 
                finally:
                    mutex.release()
                time.sleep(0.01)

def process_queue():
    while 1:
        if not q.empty():
            toSend = q.get()
            try:
                print(toSend)
                sent = s.send(toSend)
                print("{}, {}".format(sent,len(toSend)))
            except Exception as e:
                print(str(e))
                print("unable to send" + toSend.decode('utf-8')) 



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

    t = Thread( target = process_queue, args = () )
    t.start()        
    
    for device_id, device in enumerate(inputs.devices.gamepads):
        t = Thread(target = send_data, args = ( device_id, device ) )
        t.start()

