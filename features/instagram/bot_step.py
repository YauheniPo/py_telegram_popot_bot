from telegram import ParseMode

from bot import bot
from bot_constants import MSG_INSTAGRAM_POST_CONTENT, MSG_HTML_LINK
from features.instagram.insta_loader import fetch_insta_post_data


def send_to_user_insta_post_media_content(insta_post, user):
    fetch_insta_post_data(insta_post)

    bot.send_message(
        chat_id=user.user_id,
        reply_to_message_id=insta_post.message_id,
        text=MSG_INSTAGRAM_POST_CONTENT.format(insta_post.post_description,
                                               "\n".join([MSG_HTML_LINK.format(
                                                   link=link,
                                                   title="Media {}".format(title))
                                                   for title, link in
                                                   zip(range(1, len(insta_post.media_urls) + 1),
                                                       insta_post.media_urls)])),
        parse_mode=ParseMode.HTML)