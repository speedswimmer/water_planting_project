import Adafruit_DHT
from flask import Flask, render_template
import datetime, time

sensor = Adafruit_DHT.DHT22
pin = 13

def get_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    time.sleep(1)
    if humidity is not None and temperature is not None:
        return humidity, temperature

app = Flask(__name__)
@app.route('/')
def hello():
    env_data = (get_data())
    temp = round(env_data[1],3)
    humi = round(env_data[0],3)
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%Y, %H:%M")
    templateData = {
        'title' : 'Home-Server',
        'time' : timeString,
        'temp' : temp,
        'humidity' : humi
        }
    return render_template('index.html', **templateData)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
