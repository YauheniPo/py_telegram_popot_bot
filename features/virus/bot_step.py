from base.bot.bot import bot
from bot_config import covid_graph_path
from features.virus.covid19 import get_last_virus_covid_data_dir, get_location_all_virus_covid_data_dir, \
    fetch_covid_graph, get_covid_virus_msg_content
from util.logger import logger


def sent_virus_data(user):
    country = 'Belarus'
    logger().info("Get virus data for country '{}'".format(country))

    country_all_data_virus = get_location_all_virus_covid_data_dir(country)
    country_actual_data_virus = get_last_virus_covid_data_dir(
        country, country_all_data_virus)
    world_actual_data_virus = get_last_virus_covid_data_dir()

    fetch_covid_graph(country_all_data_virus, country_actual_data_virus)
    bot.send_photo(chat_id=user.user_id, photo=open(covid_graph_path, 'rb'))
    bot.send_message(
        user.user_id,
        get_covid_virus_msg_content(
            country_actual_data_virus,
            world_actual_data_virus))
