#! /usr/bin/env python3

import sys
import datetime
import os

# modify this to your time zone.
TIME_ZONE = "+0800"

# set title to command-line argument, or default
if (len(sys.argv) > 1):
    title = "-".join(sys.argv[1:])
else:
    title = "Post"

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
---
# {title}
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
    print("Post created! " + filename)
