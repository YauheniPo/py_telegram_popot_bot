# -*- coding: utf-8 -*-

start_base_cmd_text = """
{start} - HELP - telegram bot functionals
{currency} - $ / € / RUR - currency data and graph
{cinema} - cinema posters
{football} - football calendar
{instagram} - save PUBLIC Instagram post content by link"""

currency_bot_text = """
<b>{currency}</b>
<i>{currency_past_days}</i>

<b>{currency_current_day}</b>"""

cinema_bot_text = "<a href='{link}'>{title}</a> <i>{media} | {info}</i>"

football_base_cmd_text = "Please select a section."
football_bot_text = "<i>{date}</i>   <b>{host_team} -:- {guest_team}</b>"

instagram_bot_text = """
You will receive a PUBLIC post file from Instagram by sending a link to this post to the bot.
                     
Please copy/share Instagram post link and paste/ move to bot."""
instagram_warning_text_not_public = 'This Instagram post is not PUBLIC.'
instagram_warning_unknown_content_type = "Unknown content type."

error_msg_save_image = 'Save Instagram media ERROR.'