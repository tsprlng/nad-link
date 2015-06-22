NAD Link for Raspberry Pi
=====

Thanks to Morten Hustveit who [did all the work](http://www.ping.uio.no/~mortehu/nadlink/).

This works well on my C350 amp – a quick bodge connecting a GPIO pin and ground pin to an RCA connector was all that was needed. It seems happy enough with 3.3v instead of the specified 5.

Specify the correct pin in the script.

I like to do the following in my `.zshrc`:

````
alias nad='python /opt/nad-link/nad-link.py'
````

Then it's just
````
$ nad on
$ nad off
$ nad up
$ nad down
````
etc. etc.


Config
-----

Just change the YAML. Alias remote codes however you like.

I'll point you again at [Morten Hustveit's page](http://www.ping.uio.no/~mortehu/nadlink/).

For different equipment just extract the right remote codes (it's easy to enter hex into YAML). Be aware that my script expects them in normal left-to-right reading endianness (whichever that is) so just take the binary and hexify it.