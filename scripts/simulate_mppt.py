from time import time, sleep
from random import randint
import paho.mqtt.client as mqtt

def main():
    client = mqtt.Client()
    client.loop_start()

    client.connect('localhost', 1883, 60)
    try:
        while True:
            now = int(time())
            pv_power = 600 + randint(-30, 35)
            bat_temp = 25 + randint(-1, 1)
            bat_volt = (245 + randint(-1, 1))/10.0

            client.publish('battery01/mppt/power', "{} {}".format(now, pv_power), 0)
            client.publish('battery01/mppt/voltage', "{} {}".format(now, bat_volt), 0)
            client.publish('battery01/mppt/ampere', "{} {}".format(now, pv_power/bat_volt), 0)
            client.publish('battery01/mppt/temperature', "{} {}".format(now, bat_temp), 0)

            sleep(1)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    main()
