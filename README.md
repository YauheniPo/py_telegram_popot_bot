# py_telegram_popot_bot

![Python Telegram bot](https://github.com/YauheniPo/py_telegram_popot_bot/workflows/Python%20Telegram%20bot/badge.svg)

Telegram Bot **@popot_bot**

Functions:

```/start - HELP - telegram bot functionals
 /currency - $ / € / RUR - currency data and graph
 /cinema - cinema posters
 /football - football calendar
 /instagram - save Instagram post content by link
 /geo - location of the nearest ATMs
```
    

![popot_bot](https://github.com/YauheniPo/py_telegram_popot_bot/blob/master/media/ezgif.com-video-to-gif.gif)

pip install -r requirements.txt (Python 2)
pip3 install -r requirements.txt (Python 3)

python popot_bot.py


Run Telegram bot Webhook:
1) activate Webhook for bot:
https://api.telegram.org/bot<bot_token>/setWebhook?url=https://b17b8388.**_ngrok_**.io/<bot_token>
https://api.telegram.org/bot<bot_token>/setWebhook?url=https://<username>.pythonanywhere.com/<bot_token>

delete Webhook for bot:
https://api.telegram.org/bot<bot_token>/deleteWebhook

2) https://www.pythonanywhere.com/user/<username>/
- Console - New Bash
    - virtualenv venv --python=python3.8
    - source venv/bin/activate
    - clone git branch
    - pip install -r py_telegram_popot_bot/requirements.txt
- Files
- Web
    - new web app
    - Manual
    - Source code: set path_to_root_project_py_files
    - Virtualenv: set path_to_venv_folder
    - click to WSGI configuration file:
    - import sys
      path = '/home/YauheniPo/py_telegram_popot_bot'
      if path not in sys.path:
        sys.path.append(path)
      from server import app as application
    - click Save
    

flake8 --filename *.py --exclude venv
How to manually setup flake8 as PyCharm external tool

File / Settings / Tools / External Tools / Add
Name: Flake8
Program: $PyInterpreterDirectory$/python
Parameters: -m flake8 --max-complexity 10 --ignore E501 $FilePath$
Working directory: $ProjectFileDir$

Output Filters / Add
Name: Filter 1
Regular expression to match output:
$FILE_PATH$\:$LINE$\:$COLUMN$\:.*

Output Filters / Add
Name: Filter 2
Regular expression to match output:
$FILE_PATH$\:$LINE$\:.*

To check source with flake8:
Tools / External Tools / Flake8
