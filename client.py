#!/usr/bin/python3
import requests
import argparse
from config import port, host
#def if_logged():
#    return bool(requests.get('http://127.0.0.1:50000/if_logged'))


def login(subs):
    r = requests.post('http://{}:{}/login'.format(host, port), {'login': subs.login, 'password': subs.password})
    return r.text


def login_parser(subs):
    log_parser = subs.add_parser('login', description='use your login and password or print new to create them')
    log_parser.set_defaults(method='login')
    log_parser.add_argument('--login', required=True, type=str)
    log_parser.add_argument('--password', required=True, type=str)


def list_tags():
    r = requests.get('http://{}:{}/list_tags'.format(host, port))
    return r.text


def list_tags_parser(subs):
    list_parser = subs.add_parser('all-tags', description='list all tags')
    list_parser.set_defaults(method='all-tags')


def list_texts_by_tag(subs):
    r = requests.get('http://{}:{}/list_texts_by_tag?required_tag={}'.format(host, port, str(subs.tag)))
    return r.text


def texts_parser(subs):
    txt_parser = subs.add_parser('txt-by-tag', description='use existing tag to find texts')
    txt_parser.set_defaults(method='txt-by-tag')
    txt_parser.add_argument('--tag', required=True, type=str)


def make_text(subs):
    requests.post('http://{}:{}/make_own_text'.format(host, port), {'new_tag': subs.new_tag, 'new_text': subs.new_text})


def make_text_parser(subs):
    make_parser = subs.add_parser('make-text', description='write tag and text to add text to storage')
    make_parser.set_defaults(method='make-text')
    make_parser.add_argument('--new-tag', required=True, type=str)
    make_parser.add_argument('--new-text', required=True, type=str)


def exit_parser(subs):
    e_parser = subs.add_parser('exit', description='for exit')
    e_parser.set_defaults(method='exit')


def main():
    parser = argparse.ArgumentParser(description='text storage')
    subs = parser.add_subparsers()
    login_parser(subs)
    list_tags_parser(subs)
    texts_parser(subs)
    make_text_parser(subs)
    exit_parser(subs)
    r = requests.get('http://{}:{}/if_logged'.format(host, port))
    print('>> Use Your Login And Password Or Create The New One')
    while True:
        input_data = input().split()
        try:
            args = parser.parse_args(input_data)
            if args.method == 'exit':
                requests.post('http://{}:{}/unlog'.format(host, port))
                break
            if r.text == 'False':
                if args.method == 'login':
                    print('>> ' + login(args))
                    r = requests.get('http://{}:{}/if_logged'.format(host, port))
                else:
                    print('>> Login First')
            else:
                if args.method == 'all-tags':
                    print('>> ' + list_tags())
                elif args.method == 'txt-by-tag':
                    print(list_texts_by_tag(args))
                elif args.method == 'make-text':
                    make_text(args)
                elif args.method == 'login':
                    print('>> You Are Already Logged')
        except:
            print('>> wrong input')


if __name__ == '__main__':
    main()
