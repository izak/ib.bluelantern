import sys
from time import time, sleep
import paho.mqtt.client as mqtt
from threading import Thread

def _payload(ts, v):
    return "{} {}".format(ts, v)

def main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
        instance, name, serial_port):
    try:
        from serial import Serial
        from ib.victron.mk2 import MK2
    except ImportError:
        print >>sys.stderr, "ib.victron package not available"
        raise

    # Connect to MQTT broker
    client = mqtt.Client()
    client.loop_start()
    client.connect(mqtt_host, mqtt_port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username, mqtt_password)

    port = Serial(serial_port, 2400, timeout=1)
    mk2 = MK2(port).start()
    try:
        while True:
            dc_info = mk2.dc_info()
            w = dc_info.ubat * dc_info.ibat
            ts = int(time())
            client.publish('{}/{}/power'.format(instance, name), _payload(ts, w), 0)
            client.publish('{}/{}/voltage'.format(instance, name), _payload(ts, dc_info.ubat), 0)
            client.publish('{}/{}/current'.format(instance, name), _payload(ts, dc_info.ibat), 0)
            sleep(2)
    except KeyboardInterrupt:
        pass

def includeme(config):
    mqtt_host = config.registry.settings.get('mqtt.host')
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    mqtt_username = config.registry.settings.get('mqtt.username')
    mqtt_password = config.registry.settings.get('mqtt.password')

    serial_port = config.registry.settings.get('mk2.port')
    instance = config.registry.settings.get('mk2.instance')
    name = config.registry.settings.get('mk2.name')

    target = lambda: main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
        instance, name, serial_port)
    thread = Thread(target = target)
    thread.daemon = True
    thread.start()
 
if __name__ == "__main__":
    main('localhost', 1883, None, None, 'battery01', 'inverter', '/dev/ttyUSB0')
