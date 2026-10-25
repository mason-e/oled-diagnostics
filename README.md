# Raspberry Pi OLED Diagnostics Screen

This repo contains scripts and information for setting up a simple diagnostic display on a Raspberry Pi using the [SparkFun Micro OLED](https://www.sparkfun.com/sparkfun-micro-oled-breakout.html)

A shell script obtains and parses system diagnostic information (time, CPU temperature, memory usage and CPU usage), which is fed into a Python script that drives the display.

## Hardware Setup

The product page contains links to more details on preparing the breakout board. This is for the SPI configuration that the board ships in by default; I2C can be configured with soldered jumpers but was not tested. The wire colors are of course just suggestions. RST and D/C are configurable pins that can be set to any "open" GPIO in the script, but the rest use dedicated pins.

| SPI Function | Breakout Name | Wire Color | GPIO Pin |
| ------------ | ------------- | ---------- | -------- |
| GND | GND | Black | Pin 9 or 6 |
| 3.3V | VDD/3V3 | Red | Pin 1 |
| MOSI | D1 SDI | White | Pin 19 (GPIO 10) |
| SCK | D0 SCK | Green | Pin 23 (GPIO 11) |
| RST | RST | Orange | Pin 18 (GPIO 24) |
| Data/Command | D/C | Blue | Pin 16 (GPIO 23) |
| CS | CS | Purple | Pin 24 (GPIO 8) |

## Software Setup

### Enable SPI

`sudo raspi config` > Interface Options

### Python Configuration

May vary slightly based on exact model and OS version. This was tested on a Raspberry Pi 4, and required a virtual environment since `pip install` globally is disabled.

In the desired project directory, `python3 -m venv env` to set up a virtual environment, and `source env/bin/activate` to source it (terminal should change).

The main thing is installing the luma OLED library, though I found myself first hitting other dependency issues. Try these commands; if one fails, move on to another and come back for the missed ones later:

- `pip install luma.oled`
- `pip install spidev`
- `pip install rpi-lgpio`
- `sudo apt install -y swig python3-dev`
- `sudo apt install -y liblgpio-dev`

### Running

Run either `/path/to/env/bin/python /path/to/oled-diagnostics/display-diagnostics.py` from outside the activated environment, or `python display-diagnostics.py` if within. If everything is correct it should produce a display on the screen. The script is configured to run once and persist to the display after. To get fresh updates, it's recommended to schedule a service to run the script repeatedly rather than put the repetition in the script, as the latter will continuously use system resources.

## Scheduling

### Create Service

First, create a service: `sudo nano /etc/systemd/system/oled-diagnostics.service` with the following configuration (with your correct local `/path/to` and username):

```
[Unit]
Description=OLED Diagnostics
After=network.target

[Service]
Type=simple
User=USER
WorkingDirectory=/path/to/oled-diagnostics
ExecStart=/path/to/oled-diagnostics/env/bin/python /path/to/oled-diagnostics/display-diagnostics.py
Restart=no

[Install]
WantedBy=multi-user.target
```

Check if it works by running:

```
sudo systemctl daemon-reload
sudo systemctl enable --now oled-diagnostics.service
sudo systemctl start oled-diagnostics.service
```

Check status with `sudo systemctl status oled-diagnostics` or logs with `journalctl -u oled-diagnostics -f`.

### Create Schedule

If the service is confirmed to work, a schedule can be created: `sudo nano /etc/systemd/system/oled-diagnostics.timer`. This configuration updates every minute.

```
[Unit]
Description=Run OLED display update every minute

[Timer]
OnCalendar=*-*-* *:*:00
Persistent=true
Unit=oled-diagnostics.service

[Install]
WantedBy=timers.target
```

Enable the timer:
```
sudo systemctl daemon-reload
sudo systemctl enable --now oled-diagnostics.timer
```

To check it, run `systemctl list-timers`... or simply wait a minute to see the latest update on the display.