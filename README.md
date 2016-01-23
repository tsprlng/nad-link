NAD Link for Raspberry Pi
=====

Thanks to Morten Hustveit who [did all the work](http://www.ping.uio.no/~mortehu/nadlink/).

This works well on my C350 amp – a quick bodge connecting a GPIO pin and ground pin to an RCA connector was all that was needed. It seems happy enough with 3.3v instead of the specified 5.

Specify the correct pin in the script.

I like to do the following in my `.zshrc`:

````
alias nad='python /opt/nad-link/nad-link.py'
````

And on my other computers:
````
alias nad='ssh pi -t python /opt/nad-link/nad-link.py'
````
(The `-t` tells ssh to imitate a terminal so the SIGTERM from pressing `^C` is forwarded. This is helpful in order to kill the command properly, and thus stop volume changes at the intended moment before waking up the entire town.)

Then it's just
````
$ nad on
$ nad off
$ nad up
$ nad down
````
etc. etc.


Daemon
-----

I've now included an example of a very simple daemon which listens for volume control events from my Bluetooth remote (or therefore, presumably, any keyboard's volume keys) and launches the script to do the relevant volumizing.


Config
-----

Just change the config at the top of the script. Alias remote codes however you like.

I'll point you again at [Morten Hustveit's page](http://www.ping.uio.no/~mortehu/nadlink/).

For different equipment just extract the right remote codes (it's easy to enter hex into YAML). Be aware that my script expects them in normal left-to-right reading endianness (whichever that is) so just take the binary and hexify it.
