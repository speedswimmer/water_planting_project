#!/usr/bin/env python3
import time
import json
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create single-ended input on channel 0
ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads, ADS.P0)

with open("cap_config.json") as json_data_file:
    config_data=json.load(json_data_file)
# print(json.dumps(config_data))

def time_stamp():
    now=datetime.now()
    timestamp = now.strftime('%d.%m.%Y %H:%M')
    return timestamp


def percent_translation(raw_val):
    per_val = abs((raw_val-config_data["zero_saturation"])/(config_data["full_s>
    return round(per_val,3)

if __name__== '__main__':
    print("------------ {:>5}\t{:>5}\t{:>5}\n".format("Saturation", "Voltage", >
    while True:
        try:
            with open ('soil_log.txt', '+a') as file:
                point_in_time = time_stamp()
                file.write("SOIL SENSOR: " + "{:>5.2f}%\t{:>5.2f}V\t{:>5}\n".fo>
                print("SOIL SENSOR: " + "{:>5.2f}%\t{:>5.2f}V\t{:>5}".format(pe>
        except Exception as error:
            raise error
        except KeyboardInterrupt:
            print("exiting script")
        time.sleep(1800)
