flake8 --exclude=wxbot.py,snowboydetect.py,client/mic_array xiaoyun.py client
nosetests -s --exe -v --with-coverage --cover-erase
