#! /usr/bin/env python3

"""Site Manage Scripts

Usage: ./manage.py [-cgv] [input]

-c:     create post
-g:     generate static templates
-v:     do some check job
-m:     covert a normal markdown file to jekyll format
-wd:    parse weixin article meta data"""

import csv, datetime, os, sys, re
import shutil
from _manage.weixindata import write_csv

POST_PATH = os.getcwd() + "/_posts/"
POST_IMAGE_PATH = os.getcwd() + "/assets/img/posts/"
POST_IMAGE_PREFIX = "/assets/img/posts/"
FRONT_MATTER_TEMPLATE = '''\
---
layout: post
title: {title}
date: {date}
categories: 未分类
show_excerpt_image: true
---

'''



def do_check():
    """
    HTML valid or some clean job
    """
    print("HTML Valid Report (Not Implemented)")

def get_current_date():
    TIME_ZONE = "+0800"
    post_createat = datetime.datetime.now()
    short_time = post_createat.strftime('%Y-%m-%d')
    long_time = post_createat.strftime('%Y-%m-%d %H:%M:%S ') + TIME_ZONE
    return {"short": short_time, "long": long_time}

def create_post(user_input):

    if (len(user_input) > 1):
        title = "-".join(user_input)
    elif (len(user_input) == 1):
        title = user_input[0]
    else:
        title = "post"

    # standard filename format: date and title
    post_createat = get_current_date()
    filename = post_createat["short"] + "-" + title.lower().replace(" ", "-") + '.md'
    post_date = post_createat["long"]

    # create Liquid front matter
    front_matter = FRONT_MATTER_TEMPLATE.format(title=title.replace('-', ' ').capitalize(), date=post_date)

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
    CATEGORY_CSV_PATH = os.getcwd() + '/_data/archives_category.csv'
    ARCHIVES_SUBPAGE_PATH = os.getcwd() + '/_subpages/archives/'
    ARCHIVES_SUBPAGE_TEMPLATE = os.getcwd() + '/_subpages/archives.html'
    if(not os.path.exists(ARCHIVES_SUBPAGE_PATH)):
        os.mkdir(ARCHIVES_SUBPAGE_PATH)

    categories = []

    with open(CATEGORY_CSV_PATH) as csvfile:
        creader = csv.reader(csvfile)
        for category in creader:
            categories.append([category[0], category[1]])

    categories = categories[1:]

    page_template = ""

    with open(ARCHIVES_SUBPAGE_TEMPLATE) as template_file:
        page_template = template_file.read()

# 修改标题时先修改 archives.html 然后修改下方 anchor

    replace_anchor = '''title: 归档
permalink: /archives/
current_page_platform: all'''

    for category in categories:
        target_path = ARCHIVES_SUBPAGE_PATH + category[0] + ".html"

        front_matter_fragement = '''title: {0}
permalink: /archives/{1}
current_page_platform: {2}'''.format(category[1], category[0], category[0])

        with open(target_path, 'w') as write_file:
            write_file.write(page_template.replace(
                replace_anchor, front_matter_fragement))
    
    print("All archives subpage generated at: ./_subpages/archives/")

def modify_post(filepath):
    # Check file format
    if(not filepath.endswith(".md") and (not filepath.endswith(".markdown"))):
        print("Only support .md or .markdown file.")
        return

    filename = filepath.split("/")[-1]
    
    # Get file content
    md_content = ""
    with open(filepath, 'r') as md_file:
        md_content = md_file.read()
    
    # Get new filename
    post_createat = get_current_date()
    file_output_name = post_createat["short"] + "-" + filename
    file_output_path = POST_PATH + file_output_name

    post_date = post_createat["long"]
    front_matter = FRONT_MATTER_TEMPLATE.format(title=filename.replace(
        '-', ' ').capitalize().replace('.md', ""), date=post_date)
    md_content = front_matter + md_content + "\n"

    # Check if contains image tag
    IF_CONTAINS_IMAGE = "![](" in md_content

    if(IF_CONTAINS_IMAGE):
        # Move image folder to assests
        image_orig_path = "./_posts/" + filename.replace(".md", "")
        image_target_path = POST_IMAGE_PATH + filename.replace(".md", "")
        if(os.path.exists(image_orig_path)):
            shutil.move(image_orig_path, image_target_path)
            print("Image folder has been moved: " + image_target_path)
        else:
            print("Require post image folder: " + image_orig_path)

        # Replace image uri to website uri
        regex = r"!\[\w*\]\([\w\-\/\.]*\)"
        pattern = re.compile(regex)
        md_content = pattern.sub(lambda s : s.group().replace("](", "](" + POST_IMAGE_PREFIX), md_content)

    with open(file_output_path, "w") as post_md:
        post_md.write(md_content)
    os.remove(filepath)
    print("Post publised at: " + file_output_path)


if __name__ == "__main__":

    system_args = sys.argv

    if (len(system_args) <= 1):
        print(__doc__)
    elif (system_args[1] == "-c"):
        create_post(system_args[2:])
    elif (system_args[1] == "-g"):
        generate_site()
    elif (system_args[1] == "-v"):
        do_check()
    elif (system_args[1] == "-m"):
        modify_post(system_args[2])
    elif (system_args[1] == "-wd"):
        write_csv()