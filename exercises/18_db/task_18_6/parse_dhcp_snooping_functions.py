#
#Импортируем модули
import sqlite3
import os
import sys
import yaml
import re
from datetime import timedelta, datetime
#from pprint import pprint

#Модуль glob находит все пути, совпадающие с заданным шаблоном в соответствии с правилами, используемыми оболочкой Unix.
import glob

#------------------------------------------------
def create_db(db_name, db_schema):
    print(db_name, db_schema)
#------------------------------------------------

