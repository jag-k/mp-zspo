# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1137116/data/www/domashniypsiholog.ru/')
sys.path.insert(1, '/var/www/u1137116/data/www/domashniypsiholog.ru/.venv/lib/python3.7/site-packages/')

from main import app
application = app


# import sys
# import os

# INTERP = os.path.expanduser("/var/www/u1137116/data/flaskenv/bin/python")
# if sys.executable != INTERP:
#     os.execl(INTERP, INTERP, *sys.argv)
    
# sys.path.append(os.getcwd())

# from main import app as application
