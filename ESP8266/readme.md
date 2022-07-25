<div id="top"></div>
<div class="logos">
<a href="https://pulsebook.herokuapp.com/"><img src="https://github.com/piekny27/PulseBook/blob/master/testy/static/images/Pulsebook_banner.png" height="95"></a><br><br>
<a href="#"><img alt="GitHub" src="https://img.shields.io/github/license/piekny27/flask-projekt?style=flat-square">&nbsp; <img src="https://img.shields.io/website-up-down-green-red/https/pulsebook.herokuapp.com.svg?style=flat-square"></a><br><br>
<a href="https://github.com/piekny27/flask-projekt"><img src="https://img.shields.io/badge/Flask-330F63?style=for-the-badge&logo=flask&logoColor=white"> <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"><br>
<img src="https://img.shields.io/badge/adafruit-000000?style=for-the-badge&logo=adafruit&logoColor=white"> <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white"> <img src="https://img.shields.io/badge/espressif-E7352C?style=for-the-badge&logo=espressif&logoColor=white"> <img src="https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white">
</div>
<div class="other">

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Links](#links)

## Description
<a href="#"><img src="https://cdn.discordapp.com/attachments/913059546275127306/985995974436589569/untitled45.png" height="150"></a>

Source code for the pulsebook device.

The device uses the esp8266 microcontroller and the visual studio environment with the platformio framework.

## Installation
### Required software:
1. Visual Studio Code
2. VSC plugins - Platformio

### Config platformio:
After installing the Platformio, simply open the /ESP8266 folder as workspace. Platformio should create the required files.

### Build project
Just press <kbd>F5</kbd>

### Device emulation
To test the performance of the PulseBook site without using the device you can run the emulator.
```
cd ../PulseBook
python device_emu.py
```
Notice:
If you want to take full advantage of the application you need to add external services: PostrgreSQL and Cloudinary. Secret keys should be placed in the PulseBook/tests/.env file or in config vars if you are using a VPS. Currently the site is hosted on Heroku.
## Links
[Platformio](https://platformio.org/)
