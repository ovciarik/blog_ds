#!/usr/bin/env python3.6

import os

from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
from markdown import markdown

# TODO load .md file and render html template [done]
# TODO generate index from folders and files [done]

# TODO create basic template: sidebar + main window []
#     TODO create template from index.html
# TODO center that fucking css

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



@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('./static/ico/', 'favicon.ico')


@app.route('/')
def test():
    template = 'index_default.html'
    theme = 'default'

    try: 
        theme = request.args["theme"]
        if theme == 'dark':
            template = 'index_dark.html'
        if theme == 'light':
            template = 'index_light.html'
    except:
        pass

    return render_template(template, sidebar=get_index('./blog', theme), content='')


@app.route('/<path:path>')
def get_md(path):
    if path.endswith('.css'):
        print(path)
        print(path.split('/css')[-1])
        return send_from_directory('./static/css', path.split('css/')[-1])

    if path.endswith('.js'):
        print(path)
        return send_from_directory('./static/js', path.split('js/')[-1])

    file_path = './blog/{}'.format(path)

    template = 'index_default.html'
    theme = 'default'

    try: 
        theme = request.args["theme"]
        if theme == 'dark':
            template = 'index_dark.html'
        if theme == 'light':
            template = 'index_light.html'
    except:
        pass

    return render_template(template, sidebar=get_index('./blog', theme), content=gget_md(file_path))


def get_index(path, theme):

    file_list = os.walk('./blog')

    index = '[/](/)\n\n'

    for xx in file_list:
        prefix = xx[0].replace('./blog', '')
        sufix = '?theme=' + theme
        for xxx in xx[2]:
            element = prefix + '/' + xxx
            url = prefix + '/' + xxx + sufix
            index += '[{}]({})\n\n'.format(element, url)

    return markdown(index)

def gget_md(file_path):
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
