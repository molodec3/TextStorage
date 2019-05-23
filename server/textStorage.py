from peewee import *
import os
from db_config import db_name, db_user, db_password, db_host

db = PostgresqlDatabase(database=db_name, user=db_user, password=db_password, host=db_host)


class Logins(Model):
    login = CharField(primary_key=True)
    password = CharField()

    class Meta:
        database = db


class Texts(Model):
    id = AutoField()
    text_title = CharField()
    text_made = TextField()
    tag = CharField()
    owner = CharField()

    class Meta:
        database = db


class TextStorage:
    def add_login(self, login, password):
        """
        add login with assigned password to database
        :param login: str
        :param password: str
        :return:
        """
        new_login = Logins.create(login=login, password=password)
        new_login.save()

    def get_logins(self):
        """
        :return: all existing logins ever used
        """
        ans = set()
        for login in Logins.select():
            ans.add(login.login)
        return ans

    def get_password(self, current_login):
        """
        :param current_login: str
        :return: password assigned to current login
        """
        password = Logins.select().where(Logins.login == current_login).get()
        return password.password

    def get_tags(self):
        """
        :return: all tags with existing texts
        """
        ans = ''
        for tag in Texts.select(Texts.tag).group_by(Texts.tag):
            ans += str(tag.tag) + '\n'
        return ans[:-1]

    def get_texts(self, tag):
        """
        :param tag: str
        :return: list of text's ids with appropriate tag
        """
        ans = ''
        for text_id in Texts.select().where(Texts.tag == tag):
            ans += 'id: ' + str(text_id.id) + ' \n\ttitle: ' + str(text_id.text_title) + '\n'
        return ans[:-1]

    def get_text(self, current_id):
        """
        :param current_id: int
        :return: text by id
        """
        if int(current_id) <= Texts.select(fn.MAX(Texts.id)).scalar():
            return os.path.join(os.getcwd(), str(current_id))
        else:
            return 400

    def make_text(self, title, text, tag, owner):
        """
        Add text to database
        :param title: str
        :param text: str
        :param tag: str
        :param owner: str
        :return:
        """
        current_id = Texts.insert(text_title=title, tag=tag, owner=owner).execute()
        text.save(os.path.join(os.getcwd(), str(current_id)))
        new_text = Texts.update(text_made=current_id).where(Texts.id == current_id)
        new_text.execute()
