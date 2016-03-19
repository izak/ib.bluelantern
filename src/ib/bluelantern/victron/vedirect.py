import sys
from time import time
from serial import Serial
import paho.mqtt.client as mqtt
from threading import Thread

def _payload(ts, v):
    return "{} {}".format(ts, v)

def main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
        instance, name, serial_port, is_bmv=False):

    # Connect to MQTT broker
    client = mqtt.Client()
    client.loop_start()
    client.connect(mqtt_host, mqtt_port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username, mqtt_password)

    port = Serial(serial_port, 19200, rtscts=True, dsrdtr=True)
    try:
        current_voltage = 0
        while True:
            # TODO error checking
            line = port.readline().strip()
            if line:
                ts = int(time())
                try:
                    key, value = [x.strip() for x in line.split()[:2]]
                    if key == 'V':
                        current_voltage = int(value)/1000.0
                        client.publish('{}/{}/voltage'.format(instance, name),
                            _payload(ts, "{:0.2f}".format(current_voltage)), 0)
                    elif key == 'I':
                        amps = int(value)/1000.0
                        client.publish('{}/{}/current'.format(instance, name),
                            _payload(ts, "{:0.2f}".format(amps)), 0)
                        if not is_bmv:
                            # The BMV sends power figures. The BlueSolar does
                            # not, so we have to work it out ourselves.
                            client.publish('{}/{}/power'.format(instance, name),
                                _payload(ts, "{:0.2f}".format(current_voltage*amps)), 0)
                    # P only available on BMV
                    elif is_bmv and key == 'P':
                        client.publish('{}/{}/power'.format(instance, name), _payload(ts, value), 0)
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

    # Start a thread for each configured device
    count = config.registry.settings.get('vedirect.devicecount', 1)
    for n in xrange(0, int(count)):
        serial_port = config.registry.settings.get('vedirect.{}.port'.format(count))
        instance = config.registry.settings.get('vedirect.{}.instance'.format(count))
        name = config.registry.settings.get('vedirect.{}.name'.format(count))
        is_bmv = config.registry.settings.get('vedirect.{}.bmv'.format(count),
            'no').lower() in ('yes', '1', 'true')

        target = lambda: main(mqtt_host, mqtt_port, mqtt_username, mqtt_password,
            instance, name, serial_port, is_bmv)
        thread = Thread(target = target)
        thread.daemon = True
        thread.start()
 
if __name__ == "__main__":
    main('localhost', 1883, None, None, 'battery01', 'mppt', sys.argv[1])
