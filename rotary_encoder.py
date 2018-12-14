#!/usr/bin/env python3
from RPi import GPIO
from time import sleep
import mido
from math import floor

# Set up pins
clock_pin = 17
data_pin = 18
button_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up MIDI
output_port = mido.open_output()

# Define variables
STATIC = 0
INCREASE = 1
DECREASE = -1
DEBOUNCE_TIME = 0.005

DECAY = 0
RELEASE = 1
HARDNESS = 2
TREBLE = 3
MODULATION = 4
LFO = 5
VELOCITY = 6
STEREO = 7
POLY = 8
TUNING = 9
RANDOM = 10
OVERDRIVE = 11
NUMBER_OF_PARAMETERS = 12

CC = 0
VALUE = 1

SELECT = 0
EDIT = 1

# First entry is cc, second is midi value
parameters = [\
	[102, 64], # DECAY
	[103, 64], # RELEASE
	[104, 64], # HARDNESS
	[105, 64], # TREBLE
	[106, 64], # MODULATION
	[107, 84], # LFO
	[108, 32], # VELOCITY
	[109, 64], # STEREO
	[110, 64], # POLY
	[111, 64], # TUNING
	[112, 12], # RANDOM
	[113, 0]]  # OVERDRIVE



previous_clock_state = GPIO.input(clock_pin)

def read_encoder():
	global previous_clock_state

	# Read the pins
	clock_state = GPIO.input(clock_pin)
	data_state = GPIO.input(data_pin)

	# If the encoder has moved, update
	if clock_state != previous_clock_state:
		if data_state != clock_state:
			encoder = INCREASE
		else:
			encoder = DECREASE
	# Otherwise, don't update
	else:
		encoder = STATIC

	# Store the current value
	previous_clock_state = clock_state
	sleep(DEBOUNCE_TIME)

	# Return the encoder variable
	return encoder

def update_cc(encoder_value):
	global parameters
	# Update the parameter value
	parameters[current_parameter][VALUE] += encoder_value

	# Make sure it's within the parameters
	if parameters[current_parameter][VALUE] > 127:
		parameters[current_parameter][VALUE] = 127
	if parameters[current_parameter][VALUE] < 0:
		parameters[current_parameter][VALUE] = 0

	# Send the midi message
	midi_message = mido.Message('control_change', control=parameters[current_parameter][CC], value=parameters[current_parameter][VALUE])
	output_port.send(midi_message)
	print("CC {}: {}".format(parameters[current_parameter][CC], parameters[current_parameter][VALUE]))

try:
	mode = SELECT
	current_parameter = DECAY
	while True:

		# Read encoder
		encoder_value = read_encoder()

		# If encoder value has changed
		if encoder_value != 0:
			print(encoder_value)
			if mode == EDIT:
				update_cc(encoder_value)
			else:
				current_parameter = (current_parameter + encoder_value) % NUMBER_OF_PARAMETERS
				print("Current parameter: " + str(current_parameter))

		# If button pressed
		if GPIO.input(button_pin) == GPIO.LOW:
			# Toggle mode
			mode = not mode
			print("Mode toggled: " + str(mode))
			sleep(0.3)
finally:
	GPIO.cleanup()
	output_port.close()
