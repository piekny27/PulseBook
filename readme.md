<div id="top"></div>
<div class="logos">
<a href="https://pulsebook.herokuapp.com/"><img src="testy/static/images/Pulsebook_banner.png" height="95"></a><br><br>
<a href="#"><img alt="GitHub" src="https://img.shields.io/github/license/piekny27/flask-projekt?style=flat-square">&nbsp; <img src="https://img.shields.io/website-up-down-green-red/https/pulsebook.herokuapp.com.svg?style=flat-square"></a><br><br>
<a href="https://github.com/piekny27/flask-projekt"><img src="https://img.shields.io/badge/Flask-330F63?style=for-the-badge&logo=flask&logoColor=white"> <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"><br>
<img src="https://img.shields.io/badge/adafruit-000000?style=for-the-badge&logo=adafruit&logoColor=white"> <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white"> <img src="https://img.shields.io/badge/espressif-E7352C?style=for-the-badge&logo=espressif&logoColor=white"> <img src="https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white">
</div>
<div class="other">
  
## Table of contents
* [Demo page](#demo-page)
* [General info](#general-info)
* [Installation](#installation)
* [Links](#links)

## Demo page
The website can be found at https://pulsebook.herokuapp.com/
## General info
### Description
Pulsebook is a project that aims to improve and extend the functionality of the heart rate monitor. The site receives data packets that are processed and displayed on the logged-in user's dashboard. The database stores data related to the pulse, saturation and user data. It is a convenient solution for people who want to view their measurement history on a regular basis. There are also additional options that will allow us to check the condition and correct body weight, for example: <code class="language-plaintext highlighter-rouge">BMI counter</code>.
<br><br>
<a href="#"><img src="https://cdn.discordapp.com/attachments/913059546275127306/985995974436589569/untitled45.png" height="150"></a>
<br>
It is this project that uses the heart rate monitor.
## Installation
### Required software:
1. Python
2. Visual Studio Code
3. VSC plugins - Python and Pylance

### Create environment:
Open terminal: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>`</kbd> and paste:
```
cd ../PulseBook
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### Config debugger

Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> -> Debug:Select and start debugging -> Add configuration... -> Python -> Flask

### Generating the database (optional)
```
cd ../PulseBook
python db_generator.py 
```
### Device emulation (optional)
```
cd ../PulseBook
python device_emu.py
```
Notice:
If you want to take full advantage of the application you need to add external services: PostrgreSQL and Cloudinary. Secret keys should be placed in the PulseBook/tests/.env file or in config vars if you are using a VPS. Currently the site is hosted on Heroku.
## Links
[Bootstrap v5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
<br>
[Jinja documentation](https://jinja.palletsprojects.com/en/3.1.x/)
<br>
[Flask documentation](https://flask.palletsprojects.com/en/2.1.x/)
<br>
[Colors palette](https://coolors.co/0a1128-001f54-034078-1282a2-fefcfb)
<p align="right">(<a href="#top">back to top</a>)</p>
  </div>
