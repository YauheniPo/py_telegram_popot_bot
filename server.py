# -*- coding: utf-8 -*-
import logging

import flask
import telebot
from flask_sslify import SSLify

logger = logging.getLogger(__name__)

from popot_bot import bot

app = flask.Flask(__name__)
sslify = SSLify(app)
WEBHOOK_URL_PATH = "/{}".format(bot.token)


# @app.route("/")
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def index():
    logging.info("   >>> POST webhook <<<")
    # return "<h1>ddd</h1>"
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        logging.error("   !!! POST 403 !!!")
        flask.abort(403)


if __name__ == "__main__":
    app.run()
