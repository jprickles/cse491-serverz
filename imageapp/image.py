# image handling API
import sqlite3

# images = {}

def add_image(data, type, name, description):
#     if images:
#         image_num = max(images.keys()) + 1
#     else:
#         image_num = 0
#         
#     images[image_num] = [data, type]
        
    
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    row = c.fetchone()
    
    if row == None:
    	index = 0
    else:
    	index = row[0]+1
    
    db.text_factory = bytes
    vars = (index, data, type, name, description)
    db.execute('INSERT INTO image_store VALUES (?,?,?,?,?)', vars)
    
    db.commit()
    db.close()

    return index

def get_image(num):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT image, type, name, description FROM image_store WHERE i = ? LIMIT 1', (num,))
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
	
def search( info ):
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
