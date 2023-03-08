#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor, BP
from time import sleep
import math

DURATION = 0.2
VOLUME=80 # volume for each of the flute notes
SOUNDA = sound.Sound(duration=DURATION, pitch="A5", volume=VOLUME) # triggered by ts A
SOUNDB = sound.Sound(duration=DURATION, pitch="F5", volume=VOLUME) # triggered by ts B
SOUNDC = sound.Sound(duration=DURATION, pitch="D5", volume=VOLUME) # triggered by ts C
SOUNDD = sound.Sound(duration=DURATION, pitch="C5", volume=VOLUME) # triggered by ts D
TOUCH_SENSORA = TouchSensor(1)
TOUCH_SENSORB = TouchSensor(2) # 1 and 2 at the same time will trigger SOUNDD
TOUCH_SENSORC = TouchSensor(3)
EMERGENCY_STOP_SENSOR = TouchSensor(4) # this is the emergency stop sensor
NXT_MOTOR = Motor("C")
POWER_LIMIT = 50
SPEED_LIMIT = 720
DPS_1 = 100 # slowest drumming speed
DPS_2 = 200 # second drumming speed
DPS_3 = 400 # fastest drumming speed
DELAY = 0.2



wait_ready_sensors(True) # Note: Touch sensors actually have no initialization time


def play_sound(SOUND):
    """Play the sound passed to this method"""
    SOUND.play()

def detect_emergency_stop(drumming):
   """Detect emergency stop button D being pressed"""
   if EMERGENCY_STOP_SENSOR.is_pressed():
      # D is the emergency stop. Break from this process and stop motor
      NXT_MOTOR.set_dps(0)
      NXT_MOTOR.set_limits(POWER_LIMIT, 0)
      drumming = False
   return drumming

def detect_drumming(drumming):
  """Initiate drumming motion if not already drumming. We need 
  B and C pressed to begin our drumming speed at DPS_1,
  A and C to begin drumming at DPS_2, and
  A, B, and C to begin drumming at DPS_3"""
  if not TOUCH_SENSORA.is_pressed() and TOUCH_SENSORB.is_pressed() and TOUCH_SENSORC.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    drumming = True
    NXT_MOTOR.set_dps(DPS_1)
    NXT_MOTOR.set_limits(POWER_LIMIT, DPS_1)
  if TOUCH_SENSORA.is_pressed() and TOUCH_SENSORC.is_pressed() and not TOUCH_SENSORB.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    drumming = True
    NXT_MOTOR.set_dps(DPS_2)
    NXT_MOTOR.set_limits(POWER_LIMIT, DPS_2)
  if TOUCH_SENSORA.is_pressed() and TOUCH_SENSORB.is_pressed() and TOUCH_SENSORC.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    drumming = True
    NXT_MOTOR.set_dps(DPS_3)
    NXT_MOTOR.set_limits(POWER_LIMIT, DPS_3)
  return drumming

def detect_flute_notes():
  """Detect flute notes with the following logic:
  A pressed -> play sound A
  B pressed -> play sound B
  C pressed -> play sound C
  A and B pressed -> play sound D"""
  if TOUCH_SENSORA.is_pressed() and not TOUCH_SENSORB.is_pressed() and not TOUCH_SENSORC.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    # ensure ONLY touch sensor A is pressed
    print("soundA playing")
    play_sound(SOUNDA)
  if TOUCH_SENSORB.is_pressed() and not TOUCH_SENSORA.is_pressed() and not TOUCH_SENSORC.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    # ensure ONLY touch sensor B is pressed
    print("soundB playing")
    play_sound(SOUNDB)
  if TOUCH_SENSORC.is_pressed() and not TOUCH_SENSORA.is_pressed() and not TOUCH_SENSORB.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    # ensure ONLY touch sensor C is pressed
    print("soundC playing")
    play_sound(SOUNDC)           
  if TOUCH_SENSORA.is_pressed() and TOUCH_SENSORB.is_pressed() and not TOUCH_SENSORC.is_pressed() and not EMERGENCY_STOP_SENSOR.is_pressed():
    # ensure ONLY touch sensor A and B are pressed
    print("soundD playing")
    play_sound(SOUNDD)

def setup_motor():
   """Reset the motor, set the limits, set the power, and set the dps"""
   NXT_MOTOR.reset_encoder()
   NXT_MOTOR.set_limits(POWER_LIMIT, SPEED_LIMIT)
   NXT_MOTOR.set_power(0)
   NXT_MOTOR.set_dps(0)

def run():
    """The run method contains a while loop to constantly poll our input touch sensors
    and call helper methods to perform corresponding functionalities"""
    # detect all sensor functionalities in an infinite loop
    try:
        
        print("made it here")
        setup_motor()
        drumming = False
        while True:
            drumming = detect_emergency_stop(drumming)
            detect_flute_notes()
            drumming = detect_drumming(drumming)
            # sleep for delay amount of seconds
            sleep(DELAY)
    except BaseException as e:
        print(e)  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
    finally:    
        # reset once done
        print("finally")
        BP.reset_all()
        NXT_MOTOR.reset_encoder()

if __name__=='__main__':

    # call the main run function
    run()
    BP.reset_all()