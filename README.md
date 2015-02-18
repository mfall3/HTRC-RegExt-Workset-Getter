
HTRC-RegExt-Workset-Getter
==========================

Requires an OAuth bearer token from HTRC's Identity Service
Also accepts input file name and output directory name.

Useage: python3 workset-getter.py token inputfile outputDirectory

default inputfile is worksets.xml in current working directory.
default outputDirectory is /worksets within the current working directory

Reads a workset list xml file in the form that it comes from HTRC RegExt API
For each workset in the list
-Makes a call to HTRC's RegExt API for each workset.
-Writes workset xml file in the form that they come from the HTRC RegExt API
