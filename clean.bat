echo off
del gmad_path_best_guess.txt
rmdir temp
FOR /D %%G IN (*) DO (
		IF %%G NEQ python rmdir %%G
)

