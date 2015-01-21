# -*- coding: utf-8 -*-

# Copyright 2015 Magnus Johnsson, released under WTFPL v 2 as published on http://www.wtfpl.net/about/
# Originally commissioned for Gaming For Everyone and the TTT Server 'Questionable Ethics TTT'.
# You should totally check them out.

# Changelog:
# 2015-01-21 - Magnus Johnsson - Released v 0.001, which takes a statically coded collection id and downloads all the related gma files.
# end changelog

# TODO:
# Add a possibility to download a single mod
# Add support for extracting gmad's
# Handle errors
# end todo


import http.client
import json
import urllib.request


# Get a http connection to the steam api servers:
h = http.client.HTTPConnection("api.steampowered.com")

# Set up some sane defaults for our http post requests:

headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}

# Make the first request, to get a list of all 
h.request("POST", "/ISteamRemoteStorage/GetCollectionDetails/v0001/", "collectioncount=1&publishedfileids[0]=326670326", headers)
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
	
# Reset the connection:
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
	print(item["file_url"])
	urllib.request.urlretrieve(item["file_url"], "output/ds_"+ item["publishedfileid"] + ".gma")
