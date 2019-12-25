class User:

    def __init__(self, last_name, first_name, username, user_id, lang, message):
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.user_id = user_id
        self.lang = lang
        self.message_text = message.text
        self.message = message

    def __repr__(self):
        return str(self.__dict__)
