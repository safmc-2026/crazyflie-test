import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# URI to the Crazyflie to connect to
uri = 'radio://0/40/2M/E7E7E7E706'

def simple_connect():

    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")

if __name__ == '__main__':
    print("This program will connect to a Crazyflie drone, wait for 3 seconds and then disconnect.")
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    print("Connecting to Crazyflie...")
    scf = SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache'))
    scf.open_link()
    simple_connect()
    scf.close_link()
