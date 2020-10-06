#! /usr/bin/env python3

"""Site Manage Scripts

Usage: ./manage.py [-cgv] [input]

-c:     create post
-g:     generate static templates
-v:     do some check job"""

import csv
import datetime
import os
import sys


def show_usage():
    description = """Site Manage Scripts

Usage: ./manage.py [-cgv] [input]

-c:     create post
-g:     generate static templates
-v:     do some check job"""
    print(description)


def do_check():
    """
    HTML valid or some clean job
    """
    print("HTML Valid Report (Not Implemented)")


def create_post(user_input):

    if (len(user_input) > 1):
        title = "-".join(user_input)
    else:
        title = "post"

    # modify this to your time zone.
    TIME_ZONE = "+0800"

    # standard filename format: date and title
    post_createat = datetime.datetime.now()
    filename = post_createat.strftime(
        '%Y-%m-%d-') + title.lower().replace(" ", "-") + '.md'
    post_date = post_createat.strftime('%Y-%m-%d %H:%M:%S ') + TIME_ZONE

    # create Liquid front matter
    front_matter = '''\
    ---
    layout: post
    title: {title}
    date: {date}
    categories: 
    show_excerpt_image: true
    ---

    '''.format(title=title.replace('-', ' ').capitalize(), date=post_date)

    # if we're in a jekyll root, pop it in ./_posts
    if(os.path.exists(os.getcwd() + '/_posts')):
        filepath = os.getcwd() + '/_posts/' + filename
    else:
        filepath = os.getcwd() + '/' + filename

    # check if this post exists already, otherwise create and write!
    if(os.path.exists(filepath)):
        print("Looks like this post already exists: " + filepath)
    else:
        with open(filepath, 'w') as f:
            print(front_matter, file=f)
        print("Post created: ./_posts/" + filename)


def generate_site():
    CATEGORY_CSV_PATH = os.getcwd() + '/_data/works_category.csv'
    WORKS_SUBPAGE_PATH = os.getcwd() + '/subpage/works/'
    WORKS_SUBPAGE_TEMPLATE = os.getcwd() + '/subpage/works.html'
    if(not os.path.exists(WORKS_SUBPAGE_PATH)):
        os.mkdir(WORKS_SUBPAGE_PATH)

    categories = []

    with open(CATEGORY_CSV_PATH) as csvfile:
        creader = csv.reader(csvfile)
        for category in creader:
            categories.append([category[0], category[1]])

    categories = categories[1:]

    works_template = ""

    with open(WORKS_SUBPAGE_TEMPLATE) as template_file:
        works_template = template_file.read()

    replace_anchor = '''title: 作品
permalink: /works/
current_page_platform: all'''

    for category in categories:
        target_path = WORKS_SUBPAGE_PATH + category[0] + ".html"

        front_matter_fragement = '''title: {0}
permalink: /works/{1}
current_page_platform: {2}'''.format(category[1], category[0], category[0])

        with open(target_path, 'w') as write_file:
            write_file.write(works_template.replace(
                replace_anchor, front_matter_fragement))
    
    print("All Works Subpage Generate at: ./subpage/works/")


if __name__ == "__main__":
    # set title to command-line argument, or default

    system_args = sys.argv

    if (len(system_args) <= 1):
        show_usage()
    elif (system_args[1] == "-c"):
        create_post(system_args[2:])
    elif (system_args[1] == "-g"):
        generate_site()
    elif (system_args[1] == "-v"):
        do_check()
