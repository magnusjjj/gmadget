echo off
chcp 65001
if exist gmad_path_best_guess.txt (
	python\python.exe gmaddown_console.py %*
) else (
	python\python.exe guess_gmad_location.py
	python\python.exe gmaddown_console.py %*
)