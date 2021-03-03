
import sqlite3
import sys
import Adafruit_DHT
from gpiozero import MCP3008




def log_values(sensor_id, temp, hum, light):

    conn=sqlite3.connect('/var/www/lab_app/lab_app.db') 
    curs=conn.cursor()
    curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),(?), (?))""", (sensor_id,temp))
    curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", (sensor_id,hum))
    curs.execute("""INSERT INTO lightlevels values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", (sensor_id,light))
    conn.commit()
    conn.close()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
ldr = MCP3008(channel=0, clock_pin=18, mosi_pin=24, miso_pin=23, select_pin=25)
light_status = round((100-(ldr.value*100)),2)


if humidity >0 and humidity <100 and temperature is not None and light_status is not None:
    log_values("1", temperature, humidity, light_status)	
else:
    print("Erroneous Reading")
