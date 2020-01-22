# py_telegram_popot_bot

Telegram Bot **@popot_bot**
Functions:
    _/start_ - HELP - telegram bot functionals
    _/currency_ - $ / € / RUR - currency data and graph
    _/cinema_ - cinema posters
    _/football_ - football calendar
    _/instagram_ - save Instagram post content by link
    _/geo_ - location of the nearest ATMs

![Alt Text](https://github.com/YauheniPo/py_telegram_popot_bot/media/ezgif.com-video-to-gif.gif)

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
    