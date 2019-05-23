#!/usr/bin/python3
import os
import requests
import argparse
from config import port, host


class ParserHelp(argparse._HelpAction):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()


class ParserException(Exception):
    def __init__(self, parser, message):
        self.parser = parser
        self.message = message


class ArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        assert 'add_help' not in kwargs, 'add_help option is forbidden in {}'.format(self.__class__.__name__)
        super(ArgParser, self).__init__(*args, **kwargs, add_help=False)
        self.register('action', 'help', ParserHelp)

    def error(self, message):
        raise ParserException(self, message)


def login(subs):
    r = requests.post('http://{}:{}/login'.format(host, port), {'login': subs.login, 'password': subs.password})
    if r.status_code == 400:
        return r.status_code
    return r.text


def login_parser(subs):
    log_parser = subs.add_parser('login', description='use your login and password or print new to create them')
    log_parser.set_defaults(method='login')
    log_parser.add_argument('--login', required=True, type=str)
    log_parser.add_argument('--password', required=True, type=str)


def list_tags():
    r = requests.get('http://{}:{}/list_tags'.format(host, port))
    return r.text if r.text != '' else 'There is no texts created'


def list_tags_parser(subs):
    list_parser = subs.add_parser('all-tags', description='list all tags')
    list_parser.set_defaults(method='all-tags')


def list_texts_by_tag(subs):
    r = requests.get('http://{}:{}/list_texts_by_tag?required_tag={}'.format(host, port, str(subs.tag)))
    return r.text


def texts_parser(subs):
    txt_parser = subs.add_parser('txt-by-tag', description='use existing tag to find texts')
    txt_parser.set_defaults(method='txt-by-tag')
    txt_parser.add_argument('tag', type=str)


def make_text(subs, current_login):
    try:
        r = requests.post('http://{}:{}/make_own_text'.format(host, port), {'title': subs.title, 'tag': subs.tag,
                                                                            'login': current_login},
                          files={'upload_file': open(subs.text_file, 'rb')})
        return r.text
    except FileNotFoundError:
        return 'There Is No File Named {}'.format(subs.text_file)


def make_text_parser(subs):
    make_parser = subs.add_parser('make-text', description='write tag and text to add text to storage')
    make_parser.set_defaults(method='make-text')
    make_parser.add_argument('--title', required=True, type=str)
    make_parser.add_argument('--tag', required=True, type=str)
    make_parser.add_argument('--text-file', required=True, type=str)


def get_text(subs):
    r = requests.get('http://{}:{}/get_text?required_id={}'.format(host, port, str(subs.id)))
    if r.status_code == 400:
        return 'File Was Not Uploaded Yet'
    else:
        with open(os.path.join(os.getcwd(), 'DownloadedText' + str(subs.id)), 'wb') as out_file:
            out_file.write(r.content)
        return 'Successfully Downloaded To {}'.format(os.getcwd())


def get_text_parser(subs):
    get_parser = subs.add_parser('get-text', description='downloads text by current id')
    get_parser.set_defaults(method='get-text')
    get_parser.add_argument('id', type=int)


def print_text(subs):
    r = requests.get('http://{}:{}/get_text?required_id={}'.format(host, port, str(subs.id)))
    if r.status_code == 400:
        return 'File Was Not Uploaded Yet'
    else:
        return r.text


def print_text_parser(subs):
    print_parser = subs.add_parser('print-text', description='returns text by current id')
    print_parser.set_defaults(method='print-text')
    print_parser.add_argument('id', type=int)


def exit_parser(subs):
    e_parser = subs.add_parser('exit', description='for exit')
    e_parser.set_defaults(method='exit')


def main():
    parser = ArgParser(description='text storage', prog='')
    subs = parser.add_subparsers(dest='method')
    login_parser(subs)
    list_tags_parser(subs)
    texts_parser(subs)
    make_text_parser(subs)
    print_text_parser(subs)
    get_text_parser(subs)
    exit_parser(subs)
    subs.add_parser('help')
    current_login = None
    print('>> Use Your Login And Password Or Create The New One "login --login [login] --password [password]"')
    while True:
        input_data = input().split()
        try:
            args = parser.parse_args(input_data)
            if args.method == 'exit':
                break
            if current_login is None:
                if args.method == 'login':
                    response = login(args)
                    if response == 400:
                        print('>> Wrong Password')
                    else:
                        print('>> ' + response)
                        current_login = args.login
                else:
                    print('>> Login First')
            else:
                if args.method == 'all-tags':
                    print('>> ' + list_tags())
                elif args.method == 'txt-by-tag':
                    print('>> ' + list_texts_by_tag(args))
                elif args.method == 'make-text':
                    print('>> ' + make_text(args, current_login))
                elif args.method == 'get-text':
                    print('>> ' + get_text(args))
                elif args.method == 'print-text':
                    print('>> ' + print_text(args))
                elif args.method == 'login':
                    print('>> You Are Already Logged')
                elif args.method == 'help':
                    parser.print_help()
        except ParserException:
            print('>> Wrong Input')


if __name__ == '__main__':
    main()
