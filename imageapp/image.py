# image handling API
import os
import sqlite3
from StringIO import StringIO
from PIL import ImageFile, Image

ThumbnailSize = 70, 70
DefaultThumbnail = "no_thumb.png"

def add_image(data, type, name, description):
    
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    row = c.fetchone()
    
    if row == None:
    	index = 0
    else:
    	index = row[0]+1
    
    db.text_factory = bytes
    vars = (index, data, type, name, description, 0)
    db.execute('INSERT INTO image_store VALUES (?,?,?,?,?,?)', vars)
    
    db.commit()
    db.close()

    return index

def get_image(num):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT image, type, name, description, score FROM image_store WHERE i = ? LIMIT 1', (num,))
	result = c.fetchone()
	db.close()

	return result

def get_latest_image():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT image, type, name, description FROM image_store ORDER BY i DESC')
    result = c.fetchone()
    db.close()

    return result

def get_all_indexes():
	result = []
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	
	c.execute('SELECT i FROM image_store ORDER BY i ASC')
	for row in c:
		result.append(row[0])

	return result
	
def get_all_images():
	img_results = {'img' : 'img'}
	img_results['results'] = []
	db = sqlite3.connect('images.sqlite')
	c = db.cursor()
	
	c.execute('SELECT i, name, description FROM image_store ORDER BY i ASC')
	for row in c:
		result = {'index' : row[0]}
		result['name'] = row[1]
		result['desc'] = row[2]
		img_results['results'].append(result)
	db.close()
	return img_results
	
def search(info):
    img_results = {'img' : 'img'}
    img_results['results'] = []

    db = sqlite3.connect('images.sqlite')
    c = db.cursor()

    if ( info == '' or info == ' ' ):
        return img_results
    else:
    	info = '%' + info + '%'
        vars = (info, info,)
        c.execute('SELECT i, name, description FROM image_store ' +
                  'WHERE name LIKE ? ' +
                  'OR description LIKE ? ' +
                  'ORDER BY i ASC', vars)

    for row in c:
        result = {'index' : row[0]}
        result['name'] = row[1]
        result['desc'] = row[2]
        img_results['results'].append(result)
    db.close()

    return img_results

def generate_thumbnail(data):
	p = ImageFile.Parser()
	img = None
	try:
		p.feed(data)
		img = p.close()
	except IOError:
		print "Cannot generate image thumbnail"
	
	if img == None:
		dirname = os.path.join(os.path.dirname(__file__),"")
		thumbnail_path = os.path.join(dirname, DefaultThumbnail)
		return open(thumbnail_path, 'rb').read()
	else:
		fp = StringIO()
		img.thumbnail(ThumbnailSize, Image.ANTIALIAS)
		img.save(fp, format="PNG")
		fp.seek(0)
		return fp.read()


def get_score(num):
	result = get_image(num)
	return result[4]

def increase_score(num):
	if num == -1:
		return
	db = sqlite3.connect('images.sqlite')
	db.execute('UPDATE image_store SET score = score + 1 where i=(?)', (num,))
	db.commit()
	db.close()

def decrease_score(num):
	if num == -1:
		return
	db = sqlite3.connect('images.sqlite')
	db.execute('UPDATE image_store SET score = score - 1 where i=(?)', (num,))
	db.commit()
	db.close()
