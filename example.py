#!/usr/bin/python

"""
Example to get and set variables via AGI.
You can call directly this script with AGI() in Asterisk dialplan.
"""

from asterisk.agi import *
import sqlite3


agi = AGI()

agi.verbose("python agi started")


try:
    conn = sqlite3.connect('db.sqlite3')
except:
    print "I am unable to connect to the database"
# Get variable environment
extension = agi.env['agi_extension']

# Get variable in dialplan
phone_exten = agi.get_variable('PHONE_EXTEN')

# Set variable, it will be available in dialplan
agi.set_variable('EXT_CALLERID', '1')