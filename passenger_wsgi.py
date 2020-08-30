# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1137116/data/www/domashniypsiholog.ru/')
sys.path.insert(1, '/opt/python/python-3.7.6/lib/python3.7/site-packages/')

from main import app
application = app.wsgi({

})
