#!/bin/bash
echo -e "\n \n ### Starting a2j... \n"
/usr/bin/a2jmidi_bridge &
sleep 2
echo -e "\n \n ### Starting modhost... \n"
/usr/local/bin/mod-host &
sleep 2
echo -e "\n \n ### Starting ePiano... \n"
nc localhost 5555 < /home/pi/epiano_setup.txt &
sleep 2
echo -e "\n \n ### Starting rotary encoder... \n"
python3 /home/pi/rotary_encoder.py &
sleep 2
echo -e "\n \n ### Making connections... \n"
# Connect all alsa ports to a2j
for DEVICE in {1..256}; do /usr/bin/aconnect $DEVICE:0 'a2j_bridge':0; done
# Connect a2j to Effect in AND to mod-host in
/usr/bin/jack_connect a2j_bridge:capture effect_1:event_in
/usr/bin/jack_connect a2j_bridge:capture mod-host:midi_in
# Connect effect to playback
/usr/bin/jack_connect effect_1:left_out system:playback_1
/usr/bin/jack_connect effect_1:right_out system:playback_2
