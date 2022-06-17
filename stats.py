import Adafruit_SSD1306
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont


disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=4)
disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.truetype('/home/pi/Scripts/PixelOperator.ttf', 16)

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/'"
    cpu = subprocess.check_output(cmd, shell=True)
    cpu = f"CPU: {100 - float(str(cpu,'utf-8')):.1f}%"
    cmd = "free -m|awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\",$3,$2,$3*100/$2}'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell=True)

    draw.text((x, top+2), f"IP: {str(IP,'utf-8')}", font=font, fill=255)
    draw.text((x, top+18), f"{cpu} {str(temp,'utf-8')}", font=font, fill=255)
    draw.text((x, top+34), str(MemUsage, 'utf-8'), font=font, fill=255)
    draw.text((x, top+50), str(Disk, 'utf-8'), font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(10)
