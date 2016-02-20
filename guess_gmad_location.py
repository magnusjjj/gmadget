# -*- coding: utf-8 -*-

# Copyright 2015 Magnus Johnsson, released under WTFPL v 2 as published on http://www.wtfpl.net/about/
# Originally commissioned for Gaming For Everyone and the TTT Server 'Questionable Ethics TTT'.
# You should totally check them out.
# Open the registry, pray for it to find the gmad.exe place. Can't redistribute it, so sad, so sad.

import os
from winreg import *

gmadexe = "gmad.exe"

aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

keys_to_check = [r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 4000"]
keys_to_check.append(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 4000") # Thanks to fixator10! Original commit, https://github.com/fixator10/gmadget/commit/b3e766d45c50c06d1f662ff8a8381997e827d409

for key in keys_to_check:
	try:
		# See if we can find GMOD's location from the uninstall information:
		aKey = OpenKey(aReg, key)
		gmadexe_test = QueryValueEx(aKey, "InstallLocation")
		if gmadexe_test[1] == REG_SZ: # Success!
			gmadexe_test = gmadexe_test[0] + r"\bin\gmad.exe"
			if os.path.isfile(gmadexe_test):
				# Utter perfection
				gmadexe = gmadexe_test
	except:
		pass # Fail silently

fp = open("gmad_path_best_guess.txt", "w+")
fp.write(gmadexe)
fp.close()