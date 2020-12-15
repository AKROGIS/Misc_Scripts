@echo off
echo "---------------Remotes-----------------"
git remote -v
echo "---------------Branches----------------"
git branch -vv
echo "---------------Status------------------"
git status --porcelain
echo "---------------Stashes-----------------"
git stash list

rem git log --decorate --all --oneline --graph
