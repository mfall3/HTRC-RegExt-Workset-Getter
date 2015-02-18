#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# HTRC-RegExt-Workset-Getter
# ==========================
#
# Requires an OAuth bearer token from HTRC's Identity Service
# Also accepts input file name and output directory name.
#
# Useage: python3 workset-getter.py token inputfile outputDirectory
# default inputfile is worksets.xml in current working directory.
# default outputDirectory is /worksets within the current working directory
#
# Reads a workset list xml file in the form that it comes from HTRC RegExt API
# For each workset in the list
#   Makes a call to HTRC's RegExt API for each workset.
#   Writes workset xml file in the form that they come from the HTRC RegExt API
#
# workset-getter.py

from bs4 import BeautifulSoup
import os
import urllib.request
import sys

# require an OAuth bearer token for HTRC RegExt API
if len(sys.argv) > 1:
    token = sys.argv[1]
else:
    print('missing token -- Usage: python3 ' + sys.argv[0] + ' token [inputFile] [outputDirectory]')
    sys.exit(1)

# set default values for inputFile and outputDirectory

cwd = os.getcwd()

# get list worksts xml string
worksetsFilename = cwd + os.sep + 'worksets.xml'

# identify a directory to put the workset files into
worksetsDir = cwd + os.sep + "worksets"

# use provided values, if available
if len(sys.argv) > 2:
    worksetsFilename = sys.argv[2]

if len(sys.argv) > 3:
    worksetsDir = sys.argv[3]

# get list worksts xml string
worksetsFilename = '/home/colleen/worksets/workset-list-2015-02-13.xml'

# identify a directory to put the workset files into
worksetsDir = os.path.dirname(worksetsFilename) + os.sep + "worksets_20150213"

if not os.path.exists(worksetsDir):
    os.mkdir(worksetsDir)

with open(worksetsFilename) as worksetsFile:
    worksetsXmlString = worksetsFile.read()

soup = BeautifulSoup(worksetsXmlString)

# name is the title of the workset
names = soup.find_all('name')
# author is the owner of the workset
authors = soup.find_all('author')

# get each workset, and store it in a file with the naming convention title@owner.xml
for i, name in enumerate(names):

    wsFilename = worksetsDir + os.sep + name.string + '@' + authors[i].string + ".xml"
    # skip existing files
    # skip admin as an owner - it is an artificially created state, and the API cannot handle it
    if not os.path.isfile(wsFilename) and authors[i].string != "admin":

        url = "https://silvermaple.pti.indiana.edu:9443/ExtensionAPI-1.1.1-SNAPSHOT/services/worksets/" + name.string + "?author=" + \
              authors[i].string
        request = urllib.request.Request(url)
        request.add_header("Authorization", "Bearer " + token)
        request.add_header("Accept", "application/vnd.htrc-workset+xml")
        response = urllib.request.urlopen(request)

        with open(wsFilename, 'w') as wsFile:
            wsFile.write(response.read().decode('utf-8'))
