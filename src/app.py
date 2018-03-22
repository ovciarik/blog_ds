#!/usr/bin/env python3.6

import os

from flask import Flask
from flask import send_from_directory
from markdown import markdown

# TODO load .md file and render html template [done]
# TODO generate index from folders and files [done]

# TODO create basic template: sidebar + main window []
#     TODO create template from index.html

# TODO create solarized dark css theme []
# TODO create acme theme []
# TODO create hackernews theme []
# TODO create theme switcher []


# domain ovciarik.io
# alternative between github and common markdown
# no optimization till feature-complete
# blog publish -> automaticaly publish on AWS (or any other webservice)
# no DB

app = Flask(__name__)


def common_md_to_html(f):
    return markdown(f)

# list all folders and files
# generate index


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./static/css', path)


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('./static/ico/', 'favicon.ico')


@app.route('/')
def test():
    with open('./templates/index.html', 'r') as f:
        return get_index('./blog') + f.read()


@app.route('/<path:path>')
def get_md(path):
    file_path = './blog/{}'.format(path)
    return get_index('./blog') + get_md(file_path)


def get_index(path):

    file_list = os.walk('./blog')

    index = '[/](/)\n\n'

    for xx in file_list:
        prefix = xx[0].replace('./blog', '')
        for xxx in xx[2]:
            element = prefix + '/' + xxx
            index += '[{}]({})\n\n'.format(element, element)
    index += '---'

    return markdown(index)


def get_md(file_path):
    with open(file_path, 'r') as f:
        return common_md_to_html(f.read())


def generate_index(list_of_folders):
    # should return string Markdown index generated form list of folders
    pass


if __name__ == '__main__':
    x = os.walk('./blog')
    x = list(x)
    print(x)
    # print(f'{x}')
