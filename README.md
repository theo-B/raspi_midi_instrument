WIP - don't trust these instructions

Install patched JACK
  wget http://downloads.autostatic.com/rpi/jackd2/jackd2_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb
  wget http://downloads.autostatic.com/rpi/jackd2/libjack-jackd2-0_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb
  wget http://downloads.autostatic.com/rpi/jackd2/libjack-jackd2-dev_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb
  sudo dpkg -i jackd2_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb libjack-jackd2-0_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb libjack-jackd2-dev_1.9.8~dfsg.4+20120529git007cdc37-5+fixed1~raspbian1_armhf.deb
Need to ensure that this version of Jack is used. See https://wiki.linuxaudio.org/wiki/raspberrypi for help.

Install other necessary bits and bobs
  sudo pip3 install mido
Install mod-host: https://github.com/moddevices/mod-host
Install MDA plugins
Install a2jmidi

Run script on startup:
Put raspi_midi_instrument in /etc/init.d/
Run chmod 755 /etc/init.d/raspi_midi_instrument
Run sudo update-rc.d raspi_midi_instrument defaults
This script will run the optimise_for_jack.sh script (see https://wiki.linuxaudio.org/wiki/raspberrypi for where this comes from) ,
and then run the run_rhodes.sh script which starts jack, the rhodes plugin, and all necessary connections

a2jmidi_bridge starts jack for you - avoids problems with a2j not beigng able to conenct to jack server - and has nicer port names than a2jmidid
