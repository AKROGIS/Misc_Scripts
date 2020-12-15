@echo off
REM check-repos.cmd

FOR /D %%G IN (*) DO (
   echo:
   Echo =====%%G=============================
   cd %%G
   echo ---------------Remotes-----------------
   git remote -v
   echo ---------------Branches----------------
   git branch -vv
   echo ---------------Status------------------
   git status --porcelain
   rem echo ---------------Stashes-----------------
   rem git stash list
   echo:
   cd ..
)
