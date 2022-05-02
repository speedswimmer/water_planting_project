#!/usr/bin/env python3
import time
import json
import board
import busio
import smbus2
import bme280
#import adafruit_ads1x15.ads1115 as ADS
#import Adafruit_DHT
from messaging import send_email
#from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
import sys

# alte Adafruit_Kram
#sensor  = Adafruit_DHT.DHT22
#pin = 12


# Create the I2C bus
#i2c = busio.I2C(board.SCL, board.SDA)
# Create single-ended input on channel 0
#ads = ADS.ADS1115(i2c)
#chan = AnalogIn(ads, ADS.P0)

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)


with open('/home/pi/Desktop/adafruit_ads/cap_config.json', 'r') as json_data_file:
    config_data=json.load(json_data_file)
# print(json.dumps(config_data))

def time_stamp():
    now=datetime.now()
    timestamp = now.strftime('%d.%m.%Y %H:%M')
    return timestamp

#def get_temperature():
#    for i in range (0,3):
#        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
#        time.sleep(0.3)
#        if humidity is not None and temperature is not None:
#            return temperature

def percent_translation(raw_val):
    per_val = abs((raw_val-config_data["zero_saturation"])/(config_data["full_saturation"]-config_data["zero_saturation"]))*100
    return round(per_val,2)

if __name__== '__main__':
#    print("----------- {:>5}\t{:>5}\t{:>5}\t{:>5}\n".format("Saturation", "Voltage", "Temp", "Time"))
    while True:
        try:
            with open ('/home/pi/Desktop/adafruit_ads/soil_log.txt', '+a') as file:
                point_in_time = time_stamp()
#                temp = round(get_temperature(),1)
                temp = round(data.temperature, 2)
                pressure = round(data.pressure, 2)
                humidity = round(data.humidity, 2)
                file.write("SOIL SENSOR: " + "{:>5.2f}%\t{:>5.2f}V\t{:>5}°C\t{:>5}\n".format(percent_translation(chan.value), chan.voltage, temp, point_in_time))
#                print("SOIL SENSOR: " + "{:>5.2f}%\t{:>5.2f}V\t{:>5}°C\t{:>5}".format(percent_translation(chan.value), chan.voltage, temp, point_in_time))
                if percent_translation(chan.value) < 50:
                    level_value = str(percent_translation(chan.value))
                    content = "Soil Moisture is at critical level: " + level_value + "%"
                    send_email(content, "Soil Sensor Alert")
        except Exception as error:
            raise error
        except KeyboardInterrupt:
            print("exiting script...")
            sys.exit(0)
        time.sleep(3600)
