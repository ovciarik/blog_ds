#!/usr/bin/env python3.6

import os

from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
from markdown import markdown

# TODO load .md file and render html template [done]
# TODO generate index from folders and files [done]
# TODO create basic template: sidebar + main window [done]
#     TODO create template from index.html [done]
# TODO center that fucking css [done]
# TODO create solarized dark css theme [done]
# TODO create acme theme [done]
# TODO create hackernews theme [done]
# TODO create theme switcher [done]
# TODO automaticaly generate themes [done]

# TODO block quote theme bug []
# TODO save theme as cookie []
# TODO expandable file tree view []
# TODO sidebar toggle as arrow in left middle of screen []

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

def render_page(content):
    theme_name = request.args.get('theme', 'default')
    theme_location = 'css/theme_{}.css'.format(theme_name)

    sidebar_status = request.args.get('sidebar', 'on')

    if sidebar_status == 'off':
        sidebar_file = 'css/style_sidebar_off.css'
    else:
        sidebar_file = '' 

    return render_template(
        'index.html', 
        theme_file=theme_location, 
        sidebar=get_index('./blog', theme_name, sidebar_status), 
        content=content, 
        themes=get_themes(None),
        theme_name=theme_name,
        sidebar_file=sidebar_file,
        sidebar_status=sidebar_status)

@app.route('/')
def test():
    content = ''
    return render_page(content)

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
    content = gget_md(file_path)
    return render_page(content)


def get_themes(path):
    file_stuff = os.walk('./static/css')
    # print('------------------------')
    for xx in file_stuff:
        # print(xx)
        file_list = xx[2]
        # print(file_list)
        file_list = filter(lambda x: 'theme_' in x, file_list)
        # print(file_list)
        file_list = map(lambda x: x.replace('theme_', '').replace('.css', ''), file_list)
        # print(file_list)
        # print('------------------------')
        file_list = sorted(file_list)
        return file_list



def get_index(path, theme, sidebar_status):

    file_list = os.walk('./blog')

    sufix = '?theme={}&sidebar={}'.format(theme, sidebar_status)

    index = '[/](/{})\n\n'.format(sufix)

    for xx in file_list:
        prefix = xx[0].replace('./blog', '')
        for xxx in xx[2]:
            element = prefix + '/' + xxx
            url = prefix + '/' + xxx + sufix
            index += '[{}]({})\n\n'.format(element, url)

    return markdown(index)

def gget_md(file_path):
    with open(file_path, 'r') as f:
        return common_md_to_html(f.read())



# if __name__ == '__main__':
    # x = os.walk('./blog')
    # x = list(x)
    # print(x)
    # print(f'{x}')
