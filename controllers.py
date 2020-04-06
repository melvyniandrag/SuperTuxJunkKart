import inputs
from threading import Thread, Lock

mutex = Lock()

EVENTS = {
        # note to students - I had accidentally put 0, "ABS_X, 0") here and was looking for about 5-10 minutes for my typo.
        (0, "ABS_X", 0)  : "0XR", # x right
        (0, "ABS_X", 127): "0XC", # x center
        (0, "ABS_X", 255): "0XL", # x left
        (0, "ABS_Y", 0)  : "0YD", # y down
        (0, "ABS_Y", 127): "0YC", # y center
        (0, "ABS_Y", 255): "0YU", # y right
        (0, "BTN_TOP", 0):     "0AU", # A up
        (0, "BTN_TOP", 1):     "0AD", # A downa
        (0, "BTN_TRIGGER", 0): "0BU", # A up
        (0, "BTN_TRIGGER", 1): "0BD", # A downa
        (0, "BTN_TOP2", 0):    "0CU", # A up
        (0, "BTN_TOP2", 1):    "0CD", # A downa
        (0, "BTN_THUMB", 0):   "0DU", # A up
        (0, "BTN_THUMB", 1):   "0DD", # A downa
        (0, "BTN_PINKIE", 0):  "0XU", # A up
        (0, "BTN_PINKIE", 1):  "0XD", # A downa
        (0, "BTN_THUMB2", 0):  "0YU", # A up
        (0, "BTN_THUMB2", 1):  "0YD", # A downa

        (1, "ABS_X", 0)  : "1XR", # x right
        (1, "ABS_X", 127): "1XC", # x center
        (1, "ABS_X", 255): "1XL", # x left
        (1, "ABS_Y", 0)  : "1YD", # y down
        (1, "ABS_Y", 127): "1YC", # y center
        (1, "ABS_Y", 255): "1YU", # y right
        (1, "BTN_TOP", 0):     "1AU", # A up
        (1, "BTN_TOP", 1):     "1AD", # A downa
        (1, "BTN_TRIGGER", 0): "1BU", # A up
        (1, "BTN_TRIGGER", 1): "1BD", # A downa
        (1, "BTN_TOP2", 0):    "1CU", # A up
        (1, "BTN_TOP2", 1):    "1CD", # A downa
        (1, "BTN_THUMB", 0):   "1DU", # A up
        (1, "BTN_THUMB", 1):   "1DD", # A downa
        (1, "BTN_PINKIE", 0):  "1XU", # A up
        (1, "BTN_PINKIE", 1):  "1XD", # A downa
        (1, "BTN_THUMB2", 0):  "1YU", # A up
        (1, "BTN_THUMB2", 1):  "1YD", # A downa

        (2, "ABS_X", 0)  : "2XR", # x right
        (2, "ABS_X", 127): "2XC", # x center
        (2, "ABS_X", 255): "2XL", # x left
        (2, "ABS_Y", 0)  : "2YD", # y down
        (2, "ABS_Y", 127): "2YC", # y center
        (2, "ABS_Y", 255): "2YU", # y right
        (2, "BTN_TOP", 0):     "2AU", # A up
        (2, "BTN_TOP", 1):     "2AD", # A downa
        (2, "BTN_TRIGGER", 0): "2BU", # A up
        (2, "BTN_TRIGGER", 1): "2BD", # A downa
        (2, "BTN_TOP2", 0):    "2CU", # A up
        (2, "BTN_TOP2", 1):    "2CD", # A downa
        (2, "BTN_THUMB", 0):   "2DU", # A up
        (2, "BTN_THUMB", 1):   "2DD", # A downa
        (2, "BTN_PINKIE", 0):  "2XU", # A up
        (2, "BTN_PINKIE", 1):  "2XD", # A downa
        (2, "BTN_THUMB2", 0):  "2YU", # A up
        (2, "BTN_THUMB2", 1):  "2YD", # A downa

        (3, "ABS_X", 0)  : "3XR", # x right
        (3, "ABS_X", 127): "3XC", # x center
        (3, "ABS_X", 255): "3XL", # x left
        (3, "ABS_Y", 0)  : "3YD", # y down
        (3, "ABS_Y", 127): "3YC", # y center
        (3, "ABS_Y", 255): "3YU", # y right
        (3, "BTN_TOP", 0):     "3AU", # A up
        (3, "BTN_TOP", 1):     "3AD", # A downa
        (3, "BTN_TRIGGER", 0): "3BU", # A up
        (3, "BTN_TRIGGER", 1): "3BD", # A downa
        (3, "BTN_TOP2", 0):    "3CU", # A up
        (3, "BTN_TOP2", 1):    "3CD", # A downa
        (3, "BTN_THUMB", 0):   "3DU", # A up
        (3, "BTN_THUMB", 1):   "3DD", # A downa
        (3, "BTN_PINKIE", 0):  "3XU", # A up
        (3, "BTN_PINKIE", 1):  "3XD", # A downa
        (3, "BTN_THUMB2", 0):  "3YU", # A up
        (3, "BTN_THUMB2", 1):  "3YD", # A downa
}

def send_data(device_id, device):
    for elem in device:
        for event in elem:
            key = (device_id, event.code, event.state)
            if key in EVENTS.keys():
                mutex.acquire()
                try:
                    print(EVENTS[key])
                except Exeption as e:
                    pass
                finally:
                    mutex.release()

for device_id, device in enumerate(inputs.devices.gamepads):
    t = Thread(target = send_data, args = ( device_id, device ) )
    t.start()
