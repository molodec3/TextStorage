#!/usr/bin/python3
import flask
from config import port, host
import textStorage

app = flask.Flask('textStorage', template_folder='templates')
app.textStorage = textStorage.TextStorage()


@app.route('/if_logged', methods=['GET'])
def if_logged():
    return str(app.textStorage.session)


@app.route('/', methods=['GET'])
def show_page():
    return flask.render_template(
        'main.html'
    )


@app.route('/login', methods=['POST'])
def logging():
    if flask.request.form['login'] in app.textStorage.get_logins():
        if app.textStorage.get_password(flask.request.form['login']) == \
                flask.request.form['password']:
            app.textStorage.active_login = str(flask.request.form['login'])
            return 'OK'
        else:
            return 'Wrong Password'
    else:
        app.textStorage.add_login(flask.request.form['login'], flask.request.form['password'])
        return 'New Account Was Made'


@app.route('/list_tags', methods=['GET'])
def list_tags():
    return app.textStorage.get_tags()


@app.route('/list_texts_by_tag', methods=['GET'])
def list_text_by_tag():
    if flask.request.args['required_tag'] in app.textStorage.get_tags():
        return app.textStorage.get_texts(flask.request.args['required_tag'])
    else:
        return 'No Texts By That Tag'


@app.route('/make_own_text', methods=['POST'])
def make_own_text():
    app.textStorage.make_text(flask.request.form['title'], flask.request.form['text_file'],
                              flask.request.form['tag'], flask.request.form['login'])
    return 'New Text Was Added'


@app.route('/get_text', methods=['GET'])
def get_text():
    print(flask.request.args['required_id'])
    return app.textStorage.get_text(flask.request.args['required_id'])


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--port', default=50000, type=int)
    # args = parser.parse_args()

    app.run(host, port, debug=True, threaded=True)


if __name__ == '__main__':
    main()
