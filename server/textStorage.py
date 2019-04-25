import peewee


class TextStorage:
    session = False
    active_login = None

    def __init__(self):
        pass

    def add_login(self, login, password):
        """
        add login with assigned password to database
        :param login: password:
        :return:
        """
        pass

    def get_logins(self):
        """
        :return: all existing logins ever used
        """
        return ['a', 'b']

    def get_password(self, login):
        """
        :param login:
        :return: password assigned to current login
        """
        return 'a'

    def get_tags(self):
        """
        :return: all tags with existing texts
        """
        return str([1, 2, 3, 4])

    def get_text(self, tag):
        """
        :param tag:
        :return: list of texts with appropriate tag
        """
        return str(tag) + 'a'

    def make_tag(self, tag):
        """
        Add tag to database
        :param tag:
        :return:
        """
        pass

    def make_text(self, text, owner):
        """
        Add text to database
        :param text:
        :return:
        """
        pass
