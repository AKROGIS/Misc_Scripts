@echo off
REM check-repos.cmd

FOR /D %%G IN (*) DO (
   echo:
   Echo =====%%G=============================
   cd %%G
   git fetch --all
   echo:
   cd ..
)
