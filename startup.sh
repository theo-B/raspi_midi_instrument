#!/bin/bash

# This file is not set to run on login as a cron job

echo "Killing a whole bunch of random services..."

## Stop the ntp service
sudo service ntp stop

## Stop the triggerhappy service
sudo service triggerhappy stop

## Stop the dbus service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo service dbus stop

## Stop the console-kit-daemon service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo killall console-kit-daemon

## Stop the polkitd service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo killall polkitd

## Remount /dev/shm to prevent memory allocation errors
sudo mount -o remount,size=128M /dev/shm

## Kill the usespace gnome virtual filesystem daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall gvfsd

## Kill the userspace D-Bus daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall dbus-daemon

## Kill the userspace dbus-launch daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall dbus-launch

echo "Done."

echo "Disabling CPU scaling..."
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do echo -n performance | sudo tee $cpu/cpufreq/scaling_governor; done
echo "Done."

#echo "Starting jack..."
#export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket
#/usr/bin/jackd -dalsa -P &
#jackd -P70 -p16 -t2000 -dalsa -dhw:CODEC -p64 -n3 -r44100 -s &
echo "Done."

# Run amsynth
#echo "Starting amsynth..."
#AMSYNTH_NO_GUI=1 amsynth --jack_autoconnect &
#echo "Done."

#sleep 5

# Connect Q25 (client 24 port 0) to amsynth midi in (128:0)
#echo "Connecting keyboard..."
#aconnect 24:0 128:0
#echo "Done."

# run startup script for rhodes
#/home/pi/run.sh
