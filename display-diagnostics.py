from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from luma.core.render import canvas

import subprocess

result = subprocess.run(['./get-diagnostics.sh'], capture_output=True, text=True)
values = result.stdout.strip().split(',')

serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=24)
device = ssd1306(serial, width=64, height=48)
device.persist = True

with canvas(device) as draw:
    draw.text((0, 0), f"{values[0]} | {values[1]}", fill="white")
    draw.text((0, 12), f"RAM {round((int(values[2]) / int(values[3])) * 100, 2)} %:", fill="white")
    draw.text((0, 24), f"{values[2]} / {values[3]}", fill="white")
    draw.text((0, 36), f"CPU: {values[4]}", fill="white")
