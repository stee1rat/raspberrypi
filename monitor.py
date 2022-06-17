import board
import requests
import time

from adafruit_htu21d import HTU21D
from rpi_lcd import LCD


def get_request(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            response = f"ERR:{response.status_code}"
    except requests.exceptions.ConnectionError:
        response = "CON ERR"
    except requests.exceptions.ReadTimeout:
        response = "TIMEOUT"
    return response

i2c = board.I2C()
sensor = HTU21D(i2c)
lcd = LCD(bus=3)

last_updated = time.time() - 800
while True:
    if time.time() - last_updated > 600:
        weather = get_request("http://wttr.in/Moscow?format=%x+%t")
        if isinstance(weather, requests.models.Response):
            weather = weather.text.replace("°", "")
        USD = get_request("https://rub.rate.sx/1USD")
        if isinstance(USD, requests.models.Response):
            USD = f"U:{float(USD.text):.2f}"
        last_updated = time.time()
    lcd.text(f"T:{sensor.temperature:.1f}C {weather}",  1)
    lcd.text(f"H:{sensor.relative_humidity:.1f}% {USD}", 2)
    time.sleep(10)
