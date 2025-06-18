import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/40/2M/E7E7E7E706')

DEFAULT_HEIGHT = 0.5

deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)


def move_linear_simple(scf):
    mc = MotionCommander(scf, default_height=DEFAULT_HEIGHT)
    try:
        mc.take_off(DEFAULT_HEIGHT)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
    except Exception as e:
        print("FAILED -> check exception")
    finally:
        mc.stop()
        mc.land()


def take_off_simple(scf):
    mc = MotionCommander(scf, default_height=DEFAULT_HEIGHT)
    try:
        mc.take_off()
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        mc.stop()
        mc.land()
        sys.exit(1)
    finally:
        mc.stop()


def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    scf = SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache'))
    
    try:
        scf.open_link()
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                        cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Arm the Crazyflie
        scf.cf.platform.send_arming_request(True)
        time.sleep(1.0)
        move_linear_simple(scf)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scf.close_link()
