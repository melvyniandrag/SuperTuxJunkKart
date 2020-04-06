import inputs
from threading import Thread, Lock
import events

mutex = Lock()

def send_data(device_id, device):
    for elem in device:
        for event in elem:
            key = (device_id, event.code, event.state)
            if key in events.EVENTS.keys():
                mutex.acquire()
                try:
                    print(events.EVENTS[key])
                except Exeption as e:
                    pass
                finally:
                    mutex.release()

for device_id, device in enumerate(inputs.devices.gamepads):
    t = Thread(target = send_data, args = ( device_id, device ) )
    t.start()
