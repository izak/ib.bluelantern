import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    logger.info("Connected with result code "+str(rc))

    # Subscribe to all voltage/ampere notifications. Chargers will send
    # positive ampere messages. Inverters and other loads will send negative
    # ampere numbers. The voltage numbers will (hopefully) be more or less
    # the same from all sources connected to the same bank.
    client.subscribe("+/voltage")
    client.subscribe("+/ampere")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # TODO store this in app cache of numbers
    logger.info("{} {}".format(msg.topic, str(msg.payload)))

def mqtt_init(config):
    mqtt_host = config.registry.settings.get('mqtt.host')
    if mqtt_host is None:
        raise ValueError("You must set mqtt.host in your ini file")
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    mqtt_username = config.registry.settings.get('mqtt.username')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_host, mqtt_port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username,
            config.registry.settings['mqtt.password'])
    return client
