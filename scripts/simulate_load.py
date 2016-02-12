from time import sleep
from random import randint
import paho.mqtt.client as mqtt

def main():
    client = mqtt.Client()
    client.loop_start()

    client.connect('localhost', 1883, 60)
    try:
        while True:
            ac_load = 500 + randint(-25, 25)
            bat_temp = 25 + randint(-1, 1)
            bat_volt = (245 + randint(-1, 1))/10.0

            client.publish('battery01/inverter/power', str(ac_load), 0)
            client.publish('battery01/inverter/voltage', '230', 0)
            client.publish('battery01/inverter/ampere', str(ac_load/230.0), 0)

            sleep(1)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    main()
