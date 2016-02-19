import sys
from time import sleep
import paho.mqtt.client as mqtt

def main():
    try:
        from serial import Serial
        from ib.victron.mk2 import MK2
        from ib.victron.scripts.options import parser, options
    except ImportError:
        print >>sys.stderr, "ib.victron package not available"
        raise

    # Connect to MQTT broker
    # TODO, extend parser and add options for hostname and port
    client = mqtt.Client()
    client.loop_start()
    client.connect('localhost', 1883, 60)

    port = Serial(options.port, options.baudrate, timeout=options.timeout)
    mk2 = MK2(port)
    # TODO, extend options to configure instance and equipment name
    try:
        while True:
            dc_info = mk2.dc_info()
            w = dc_info.ubat * dc_info.ibat
            client.publish('battery01/inverter/power', str(w), 0)
            client.publish('battery01/inverter/voltage', str(dc_info.ubat), 0)
            client.publish('battery01/inverter/ampere', str(dc_info.ibat), 0)
            sleep(2)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
