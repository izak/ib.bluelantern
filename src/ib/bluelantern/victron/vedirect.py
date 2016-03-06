import sys
from time import time
from serial import Serial
import paho.mqtt.client as mqtt
from threading import Thread

def _payload(ts, v):
    return "{} {}".format(ts, v)

def main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
        instance, name, serial_port):

    # Connect to MQTT broker
    client = mqtt.Client()
    client.loop_start()
    client.connect(mqtt_host, mqtt_port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username, mqtt_password)

    port = Serial(serial_port, 115200, rtscts=True, dsrdtr=True)
    try:
        while True:
            # TODO error checking
            line = port.readline().strip()
            if line:
                ts = int(time())
                try:
                    key, value = [x.strip() for x in line.split()[:2]]
                    if key == 'P':
                        client.publish('{}/{}/power'.format(instance, name), _payload(ts, value), 0)
                    elif key == 'V':
                        client.publish('{}/{}/voltage'.format(instance, name), _payload(ts, "{:0.2f}".format(int(value)/1000.0)), 0)
                    elif key == 'I':
                        client.publish('{}/{}/ampere'.format(instance, name), _payload(ts, "{:0.2f}".format(int(value)/1000.0)), 0)
                except ValueError:
                    print "Malformed line: {}".format(line)
    except KeyboardInterrupt:
        pass
    port.close()

def includeme(config):
    mqtt_host = config.registry.settings.get('mqtt.host')
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    mqtt_username = config.registry.settings.get('mqtt.username')
    mqtt_password = config.registry.settings.get('mqtt.password')

    serial_port = config.registry.settings.get('vedirect.port')
    instance = config.registry.settings.get('vedirect.instance')
    name = config.registry.settings.get('vedirect.name')

    target = lambda: main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
        instance, name, serial_port)
    thread = Thread(target = target)
    thread.daemon = True
    thread.start()
 
if __name__ == "__main__":
    main('localhost', 1883, None, None, 'battery01', 'mppt', sys.argv[1])
