# RaspberryPi Newsticker

## What do you need?
- 3x RGB Full-Color LED Matrix Panel Display 64×32 Pixels
- 1x Raspberry Pi or Raspberry Pi Zero
- 1x 5V Powersupply (minimum 2A) 
- Wirering for all Components

## Wirering

![](https://github.com/pascalpradel/RaspberryPi_Newsticker/blob/main/Images/Wirering.PNG)

## Installation

- Installation of all requiered Features:
  
    `sudo apt-get update && sudo apt-get upgrade -y`

    `sudo apt install git-all -y`

    `sudo git clone https://github.com/hzeller/rpi-rgb-led-matrix`

    `sudo nano /boot/config.txt`

- set "dtparam-audio=on" to "dtparam=audio=off" -> then Exit with Str + x

    `sudo nano /etc/modprobe.d/raspi-blacklist.conf`

- add `blacklist snd_bcm2835` -> then Exit with Str + x

    `sudo reboot`

    `cd rpi-rgb-led-matrix`

    `sudo make`

    `sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y`

    `sudo make build-python PYTHON=$(command -v python3)`

    `sudo make install-python PYTHON=$(command -v python3)`

#### Matrix Example #1:

- Change Directory and start the demo Skript (if you have only one led matrix, use `-led-cols=64`)

    `cd /rpi-rgb-led-matrix/examples-api-use`

    `sudo ./demo -D 9 –led-rows=32 –led-cols=192`

#### Matrix Example #2:

- Change Directory and start the demo Skript (if you have only one led matrix, use `--led-cols=64`)

    `cd /rpi-rgb-led-matrix/bindings/python/samples`

    `sudo python runtext.py`

- Reboot after Testing a Example or both :D
  
    `sudo reboot`

### Installation of Newsticker

- Clone this Repository and set up a Linux service, that it runs on boot (in this case bewteen 8AM and 10PM)

    `sudo git clone https://github.com/pascalpradel/RaspberryPi_Newsticker`

    `cd /RaspberryPi_Newsticker/CODE`

#### Newsticker Settings

- Now you can change the Settings of the Newsticker

    `nano RaspberryPiNewsticker.py` and then exit with Str + X

    - `SHUFFLE = True` displayes the data from displayData.json in and random order

    - `LIVEREQUEST = True` retrieves the data with a thread right before it gets displayed (not recommened for Raspberry Pi Zero)

    - `ROWS = 32` number of pixel rows of the matrix

    - `COLS = 192` number if pixel cols of the matrix
  
    - `BRIGHTNESS = 50` brightness in %
  
    - `FONT = "fonts/Calibri-26.bdf"` font that gets used
  
    - `TEXTCOLOR = [0, 255, 0]` color of the text in rgb code

- Add a Open Weather Map API Key to `config.json`

    `nano config.json` enter the key and then exit with Str + X

- Add or Edit the Display Data

    `nano displayData.json` -> edit, then exizt with Str + X

    - type is stock, index, reuters or weather
    - feel free to add your own custom api or web scraper

#### Service and Timer

- Add a Service and a Timer

    `chmod +x RaspberryPiNewsticker.py`

    `sudo nano /etc/systemd/system/script-runner.service`

- Enter following code and Save with Str + X

    ```python
    [Unit]
    Description=Python script runner
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=python /home/pi/RaspberryPi_Newsticker/CODE/RaspberryPiNewsticker.py
    WorkingDirectory=/home/pi/RaspberryPi_Newsticker/CODE
    Restart=always
    User=root

    [Install]
    WantedBy=multi-user.target
    ```

    `sudo chmod 644 /etc/systemd/system/script-runner.service`

    `sudo systemctl daemon-reload`

    `sudo systemctl enable script-runner.service`

    `sudo nano /etc/systemd/system/script-runner.timer`

- Enter following code and Save with Str + X
  
    ```python
    [Unit]
    Description=Run script-runner.service between 8AM and 10PM

    [Timer]
    OnCalendar=*-*-* 08:00:00
    OnCalendar=*-*-* 22:00:00
    Unit=script-runner.service

    [Install]
    WantedBy=timers.target
    ```

    `sudo systemctl enable script-runner.timer`

    `sudo systemctl start script-runner.timer`

    `sudo reboot`

- After the reboot the Newsticker starts automaticly 

- If not you can see with following command, if the service is running:

    `sudo systemctl status script-runner`