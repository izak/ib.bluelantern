from time import sleep
from random import randint
import paho.mqtt.client as mqtt

def main():
    client = mqtt.Client()
    client.loop_start()

    client.connect('localhost', 1883, 60)
    try:
        while True:
            pv_power = 600 + randint(-30, 35)
            bat_temp = 25 + randint(-1, 1)
            bat_volt = (245 + randint(-1, 1))/10.0

            client.publish('battery01/mppt/power', str(pv_power), 0)
            client.publish('battery01/mppt/voltage', str(bat_volt), 0)
            client.publish('battery01/mppt/ampere', str(pv_power/bat_volt), 0)
            client.publish('battery01/mppt/temperature', str(bat_temp), 0)

            sleep(1)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    main()
