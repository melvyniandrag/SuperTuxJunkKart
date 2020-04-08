# SuperTuxJunkKart

Little project aimed at turning a cardboard box into a wireless 4 player arcade-style controller. This is a time wasting project because we're stuck inside on acct of coronavirus and we have alot of cardboard boxes so we're seeing what fun stuff we can make with them.

Got 4 cheap aliExpress game joystick+button sets. Plugged them into a raspberry pi. The Raspberry pi connects to a "game console" via a TCP socket and sends button press events. The "console" sends these button press events to the game. The "console" is a thinkpad which is for now running SuperTuxKart. In the future I'll connect this to a retroarch setup. Tried installing retropie/retroarch on my old Thinkpad T410 but it encounters and error during installation. Install works fine on raspberry pi but, alas, the raspberry pi is being used as a radio transmitting device to send the button press events.

Want to program this raspberry pi to act as a bluetooth HID device such as a game pad but can't get the damned thing to work on Linux. Sending the button press events via a tcp socket required not more than an hour's thought to get 99% working. And so that's why it's programmed that way.

![controller opened](game.jpg)
