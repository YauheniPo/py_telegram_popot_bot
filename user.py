class User:

    def __init__(self, last_name, first_name, username, user_id, lang, message):
        self._last_name = last_name
        self._first_name = first_name
        self._username = username
        self._user_id = user_id
        self._lang = lang
        self._message_text = message.text
        self._message = message

    def get_last_name(self):
        return self._last_name

    def get_first_name(self):
        return self._first_name

    def get_username(self):
        return self._username

    def get_user_id(self):
        return self._user_id

    def get_lang(self):
        return self._lang

    def get_message(self):
        return self._message

    def get_message_text(self):
        return self._message_text

    def __repr__(self):
        return str(self.__dict__)


class OnlyOne:
    class __OnlyOne:

        def __str__(self):
            return repr(self)
    instance = None

    def __init__(self):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.instance, key, value)
