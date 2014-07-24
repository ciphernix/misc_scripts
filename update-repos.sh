#!/bin/bash
REPOS=/home/ciphernix/Dropbox/repos/
for repo in $( find $REPOS -maxdepth 1 -type d | grep -v "git" )                     ; do
        echo $repo
        cd ${repo}
        git pull origin master
        git add *
        git commit -am "Scrippted commit" && git push origin mas                     ter
done
