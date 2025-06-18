import logging
import time
import sys

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/40/2M/E7E7E7E706'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def simple_log(scf, logconf):

    logger = SyncLogger(scf, logconf)
    logger.connect()
    for log_entry in logger:
        timestamp = log_entry[0]
        data = log_entry[1]
        logconf_name = log_entry[2]
        print('[%d][%s]: %s' % (timestamp, logconf_name, data))
        break
    logger.disconnect()

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')
    lg_stab.add_variable('pm.vbat', 'float')

    scf = SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache'))
    try:
        scf.open_link()
        simple_log(scf, lg_stab)
    except Exception as e:
        print("FAILED -> check exception: %s" % e)
    finally:
        scf.close_link()
        sys.exit(1)



