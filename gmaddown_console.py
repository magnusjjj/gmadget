# -*- coding: utf-8 -*-
 
# Copyright 2015 Magnus Johnsson, released under WTFPL v 2 as published on http://www.wtfpl.net/about/
# Originally commissioned for Gaming For Everyone and the TTT Server 'Questionable Ethics TTT'.
# You should totally check them out.
 
# Changelog:
# 2015-01-21 - Magnus Johnsson - Released v 0.001, which takes a statically coded collection id and downloads all the related gma files.
# 2016-01-16 - Fixed numerous bugs, and made it actually usable. Released it to the public.
# end changelog
 
import http.client
import json
import urllib.request
import argparse
import sys
import lzma
import os
import subprocess
from winreg import *
 
gmadexe = ""
try:
    # This file should have been generated  by guess_gmad_location.py :). Should contain the path to gmad.exe
    with open("gmad_path_best_guess.txt", "r") as gmadread:
        gmadexe = gmadread.read()
except:
    pass
 
if gmadexe == "":
    print("Sorry, but gmad_path_best_guess.txt does not exist! Run guess_gmad_location.py or create manually with only the path to gmad.exe as content!")
# First we parse the command line options
 
parser = argparse.ArgumentParser(description='Tool for downloading gmad files')
parser.add_argument('--collectionid', dest='collectionid', help='The collection id, from the url of the collection', metavar='ID', type=int)
parser.add_argument('--singleids', dest='singleids', help='The ids for a single mods, from the url of the mods.',metavar='ID', type=int, nargs='+')
parser.add_argument('--temp', dest='output', help='The temp directory', default='./temp/')
parser.add_argument('--noextract', dest='noextract', help="Don't try extract the gmad files", default='N', const='Y', action='store_const')
 
settings = vars(parser.parse_args())
 
# Make sure that the temp directory exists
d = os.path.dirname(settings["output"])
if not os.path.exists(d):
    os.makedirs(d)
 
if settings["collectionid"] is None and settings["singleids"] is None:
    print("You have to specify a collection id, or one or several single mod ids. See '--help'")
    sys.exit()
 
# Get a http connection to the steam api servers:
h = http.client.HTTPConnection("api.steampowered.com")
 
# Set up some sane defaults for our http post requests:
 
headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
 
           
# Below, the code inside the if's create a list of mod id's to download
           
params = ""
           
if settings["collectionid"] is not None:
 
    print("Getting a list of the mods inside collection id " + str(settings["collectionid"]))
    # Make the first request, to get a list of all
    h.request("POST", "/ISteamRemoteStorage/GetCollectionDetails/v0001/", "collectioncount=1&publishedfileids[0]=" + str(settings["collectionid"]), headers)
    response = h.getresponse()
    data1 = response.read()
 
    # The response will be JSON
    json_demystified = json.loads(data1.decode("utf-8"))
    # Scrub the response a bit
    json_demystified = json_demystified["response"]["collectiondetails"][0]["children"];
 
 
    # Lets create the request for a complete file list. You can download multiple descriptions at once, like so:
 
    i = 0
   
    params = "itemcount=" + str(len(json_demystified))
 
    for item in json_demystified:
        itemid = item["publishedfileid"]
        params += "&publishedfileids[" + str(i) + "]="+itemid
        i += 1
   
if settings["singleids"] is not None:
    i = 0
   
    params = "itemcount=" + str(len(settings["singleids"]))
 
    for item in settings["singleids"]:
        params += "&publishedfileids[" + str(i) + "]="+str(item)
        i += 1
 
# We should now, from the above, have a list of mod id's to download
   
# Reset the connection (if any):
h = http.client.HTTPConnection("api.steampowered.com")
 
# Send a request for a file list:
h.request("POST", "/ISteamRemoteStorage/GetPublishedFileDetails/v0001/", params, headers)
response = h.getresponse()
 
data1 = response.read()
 
# Decode json and scrub:
json_demystified = json.loads(data1.decode("utf-8"))
json_demystified = json_demystified["response"]["publishedfiledetails"]
 
# And download all the files into a subdirectory:
for item in json_demystified:
    try:
        print("Downloading " + item["file_url"] + " (" + item['title'] + ") to " + settings["output"] + "ds_"+ item["publishedfileid"] + ".gma")
    except:
        print("The mod you tried to download is probably not a garrys mod mod. It has no file url, so we can't actually download it. Below is a dump of the info we got from steam:")
        print(item)
        input("Press enter to continue")
        continue
   
    file_savename = settings["output"] + "ds_"+ item["publishedfileid"] + ".gma"
    if os.path.exists(file_savename):
        print("This mod is already downloaded! Continuing..")
        continue
        #os.remove(file_savename)
   
    urllib.request.urlretrieve(item["file_url"], file_savename)
   
    try:
        if settings["noextract"] != 'Y':
            with lzma.open(file_savename) as f:
                with open(file_savename + ".out", "wb+") as fout:
                    fout.write(f.read())
    except (lzma.LZMAError, EOFError):
        print("This mod has broken compression. Can't extract it automatically, so you will have to take a peek at it manually.")
        input("Press enter to continue")
        continue
    subprocess.check_output([gmadexe, "extract", "-file", file_savename + ".out", "-out", item['title']])
