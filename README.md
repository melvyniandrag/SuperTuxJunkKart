# SuperTuxJunkKart

Little project aimed at turning a cardboard box into a wireless 4 player arcade-style controller. This is a time wasting project because we're stuck inside on acct of coronavirus and we have alot of cardboard boxes so we're seeing what fun stuff we can make with them.

Main idea is this controller must be wireless because my kids are 5 and they trip over everything and bounce and run all day. Don't want the thing plugged into the tv and pulling the tv over when they inevitably trip over a wire. 

Got 4 cheap aliExpress game joystick+button sets. Plugged them into a raspberry pi. The Raspberry pi connects to a "game console" via a TCP socket and sends button press events. The "console" sends these button press events to the game. The "console" is a thinkpad which is for now running SuperTuxKart. In the future I'll connect this to a retroarch setup. Tried installing retropie/retroarch on my old Thinkpad T410 but it encounters and error during installation. Install works fine on raspberry pi but, alas, the raspberry pi is being used as a radio transmitting device to send the button press events.

Want to program this raspberry pi to act as a bluetooth HID device such as a game pad but can't get the damned thing to work on Linux. Sending the button press events via a tcp socket required not more than an hour's thought to get 99% working. And so that's why it's programmed that way.

![controller opened](game.jpg)

## The code
There are some EVENTS like these:

```
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
```

these describe joystick movements ( ABS_X and ABS_Y ) and Button press events. Each event is translated to a 3 character code e.g. 0YD = "player 0, y axis down" and set from the raspberry pi to the system playing the game via TCP.
