#!/usr/bin/env python3.6

import os

from flask import Flask
from markdown import markdown

# TODO load .md file and render html template
# generate index from folders and files

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


@app.route('/')
def test():
    with open('./blog/hello.md', 'r') as f:
        return common_md_to_html(f.read())


@app.route('/<path:path>')
def get_md(path):
    file_path = './blog/{}'.format(path)
    return get_index('./blog') + get_md(file_path)


def get_index(path):

    file_list = os.walk('./blog')

    index = ''

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
