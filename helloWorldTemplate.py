import Adafruit_DHT
from flask import Flask, render_template
import datetime

sensor = Adafruit_DHT.DHT22
pin = 13

def get_data():
    humidity, temperatue = Adafruit_DHT.read_retry(sensor, pin)
    time.sleep(1.5)
    if humidity is not None and temperature is not None:
        return humidity, temperature

app = Flask(__name__)
@app.route('/')
def hello():
    temp = round(get_data)
    #
    #
    #
    #
    #
    #
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d, %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time' : timeString
        }
    return render_template('index.html', **templateData)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)