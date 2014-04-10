# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher
import sqlite3
import os

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
    if not os.path.exists('./images.sqlite'):
		db = sqlite3.connect('images.sqlite')
		db.execute('CREATE TABLE IF NOT EXISTS image_store' + 
					'(i INTEGER PRIMARY KEY, image BLOB, type TEXT,' + 
	    			'name TEXT, description TEXT)')

		some_data = open('imageapp/dice.png', 'rb').read()
		image.add_image(some_data, 'png', 'Dice brah', 'Default Image')

		db.commit()
		db.close()
    

def teardown():                         # stuff that should be run once.
    pass
