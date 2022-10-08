# -*- encoding: utf-8 -*-
# 
import os, sys


INTERP = os.path.expanduser("/var/www/u1741276/data/flaskenv/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from main import application

