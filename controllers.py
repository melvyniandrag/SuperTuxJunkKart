import queue
import inputs
from threading import Thread, Lock
import events
import socket, select
import sys

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


def send_data(device_id, device):
    for elem in device:
        for event in elem:
            key = (device_id, event.code, event.state)
            if key in events.EVENTS.keys():
                if event.state != 127 and  event.code == "ABS_X" and already_sent_left_right[device_id]:
                    continue
                elif event.state != 127 and  event.code == "ABS_X" and not already_sent_left_right[device_id]:
                    continue
                    already_sent_left_right[device_id] = True
                elif event.state == 127 and  event.code == "ABS_X"  and already_sent_left_right[device_id]:
                    continue
                    already_sent_left_right[device_id] = False
                elif event.state == 127 and event.code == "ABS_X" and not already_sent_left_right[device_id]:
                    continue
                elif event.state != 127 and  event.code == "ABS_Y" and already_sent_up_down[device_id]:
                    continue
                elif event.state != 127 and  event.code == "ABS_Y" and not already_sent_up_down[device_id]:
                    continue
                    already_sent_up_down[device_id] = True
                elif event.state == 127 and  event.code == "ABS_Y"  and already_sent_up_down[device_id]:
                    continue
                    already_sent_up_down[device_id] = False
                elif event.state == 127 and event.code == "ABS_Y" and not already_sent_up_down[device_id]:
                    continue
                while 1:
                    if not mutex.locked():
                        mutex.acquire()
                        break;
                    else:
                        time.sleep(0.005)
                try:
                    q.put(events.EVENTS[key].encode('utf-8'))
                except Exception as e:
                    print(str(e))
                    print("unable to send" + events.EVENTS[key]) 
                finally:
                    mutex.release()

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

