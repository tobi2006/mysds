rsync -ave ssh --exclude-from 'exclude.txt' . tobi@tobiaskliem.de:/home/tobi/cccu
ssh -t tobiaskliem.de "rm database/*.pyc; rm mysds/*.pyc; rm export/*.pyc; rm anonymous_marking/*.pyc; sudo service apache2 restart"
