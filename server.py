# -*- coding: utf-8 -*-
import logging

import flask
import telebot
from flask_sslify import SSLify

logger = logging.getLogger(__name__)

from popot_bot import bot, TELEGRAM_BOT_NAME, TELEGRAM_BOT_TOKEN

app = flask.Flask(__name__)
sslify = SSLify(app)
WEBHOOK_URL_PATH = "/{}".format(TELEGRAM_BOT_TOKEN)


@app.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    time.sleep(0.1)
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(TELEGRAM_BOT_NAME, TELEGRAM_BOT_TOKEN))
    return "Set Webhook!", 200


@app.route('/deleteWebhook', methods=["GET"])
def index():
    bot.remove_webhook()
    return "Remove Webhook!", 200


# @app.route("/")
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    logging.info("   >>> POST webhook <<<")
    # return "<h1>ddd</h1>"
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    else:
        logging.error("   !!! POST 403 !!!")
        flask.abort(403)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
