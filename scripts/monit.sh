#!/bin/bash
#dir=public/upload/alprVideo.mp4
commit_repo ()
{
commit_message1="$1"
commit_message2="$2"
commit_message3="$3"
commit_message3="$4"
commit_message3="$5"
git add . -A
git commit -m "$commit_message1 $commit_message2 $commit_message3 $commit_message4 $commit_message5"
git push
}


dir=instance/
#inotifywait -m "$dir" -e close_write --format '%w%f' |
inotifywait -m "$dir" -e close_write --format '%:e %f' |
    while IFS=' ' read -r fname
    do
        [ -f "$fname" ] && ls "$fname"
        pwd
        echo $USER
        #commit_repo added inotfy monit
    done

 #for file in tmp/images/*.jpg; do   ls -la | sha1sum "$file" ; done