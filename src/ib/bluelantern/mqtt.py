import logging
import paho.mqtt.client as mqtt
from ib.bluelantern.event import MetricReceived, ChargeMetricReceived, DischargeMetricReceived

logger = logging.getLogger(__name__)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    logger.info("Connected to MQTT broker with result code "+str(rc))

    # Subscribe to all voltage/current notifications. Chargers will send
    # positive current messages. Inverters and other loads will send negative
    # current numbers. The voltage numbers will (hopefully) be more or less
    # the same from all sources connected to the same bank.
    client.subscribe("+/+/voltage")
    client.subscribe("+/+/current")
    client.subscribe("+/+/power")
    client.subscribe("+/+/temperature")

# The callback for when a PUBLISH message is received from the server.
def on_message_maker(cache, registry):
    def on_message(client, userdata, msg):
        instance, id, unit = msg.topic.split('/')[:3]
        assert unit in ('voltage', 'current', 'power', 'temperature'), \
            "Unknown unit"
        try:
            timestamp, value = msg.payload.split()
            value = float(value)
            cache[instance][id][unit] = value
            timestamp = int(timestamp)
        except KeyError:
            logger.error("Failed to find equipment for {}".format(msg.topic))
        except ValueError:
            logger.error("Cannot convert value {} to float for {}".format(msg.payload, msg.topic))
        else:
            t = cache[instance][id]['type']
            if t in ('pv', ):
                registry.notify(ChargeMetricReceived(instance, id, t,
                    timestamp, unit, value))
            elif t in ('load', ):
                registry.notify(DischargeMetricReceived(instance, id, t,
                    timestamp, unit, value))
            else:
                registry.notify(MetricReceived(instance, id, t,
                    timestamp, unit, value))
    return on_message

def mqtt_init(config, cache):
    mqtt_host = config.registry.settings.get('mqtt.host')
    if mqtt_host is None:
        raise ValueError("You must set mqtt.host in your ini file")
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    mqtt_username = config.registry.settings.get('mqtt.username')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message_maker(cache, config.registry)

    client.connect(mqtt_host, mqtt_port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username,
            config.registry.settings['mqtt.password'])
    return client
