from peewee import *
from db_config import db_name, db_user, db_password, db_host

db = PostgresqlDatabase(database=db_name, user=db_user, password=db_password, host=db_host)


class Logins(Model):
    login = CharField(primary_key=True)
    password = CharField()
    texts_added = IntegerField()

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
        new_login = Logins.create(login=login, password=password, text_added=0)
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
        try:
            Texts.select(Texts.tag).where(Texts.id == current_id).get()
            f = open(current_id, 'r')
            text = f.read()
            return text
        except IndexError:
            return 'No texts with that id'

    def make_text(self, title, text, tag, owner):
        """
        Add text to database
        :param title: str
        :param text: str
        :param tag: str
        :param owner: str
        :return:
        """
        count = Logins.select().where(Logins.login == owner).get()
        user = Logins.update(texts_added=count.texts_added + 1).where(Logins.login == owner)
        user.execute()
        new_text = Texts.create(text_title=title, text_made='tmp', tag=tag, owner=owner)
        new_text.save()
        new_text = Texts.select().where(Texts.text_made == 'tmp').get()
        current_id = new_text.id
        f = open(str(current_id), 'w')
        f.write(text)
        f.close()
        new_text = Texts.update(text_made=current_id).where(Texts.text_made == 'tmp')
        new_text.execute()
