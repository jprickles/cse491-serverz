import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')
    
    @export(name='home')
    def home(self):
    	return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        f_name   = request.form['name']
        f_desc   = request.form['description']
        
        fileType = ( the_file.base_filename.split('.')[1] ).lower()
        if fileType == 'tiff' or fileType == 'tif':
        	fileType = 'tiff'
        elif fileType == 'jpeg' or fileType == 'jpg':
        	fileType = 'jpg'
        
        print 'received file of type: ' + fileType
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, fileType, f_name, f_desc)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='viewThumb')
    def viewThumb(self):
		
		request = quixote.get_request()
		response = quixote.get_response()
		the_int = int(request.form['i'])
		
		results = {"image": the_int}
		
		return html.render('viewThumb.html', results)

    @export(name='list')
    def list(self):
    	results = image.get_all_images()
        return html.render('list.html', results )

    @export(name='thumbnails')
    def thumbnails(self):
    	results = image.get_all_images()
        return html.render('thumbnails.html', results )

    @export(name='search')
    def search(self):
    	return html.render('search.html')
    
    @export(name='result')
    def result(self):
    	response = quixote.get_request()
    	
    	info = response.form['query']
    	
    	results = image.search(info)
    	return html.render('result.html', results)

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        img = image.get_latest_image()
        print img[1]
        response.set_content_type('image/%s' % img[1])
        
        return img[0]
    
    @export(name='get_image')
    def get_im(self):
		request = quixote.get_request()
		response = quixote.get_response()
	
		the_int = int(request.form['special'])
		img = image.get_image(the_int)
		
		response.set_content_type('image/%s' % img[1])
		return img[0]

    @export(name='get_thumbnail')
    def get_thumb(self):
        request = quixote.get_request()
        response = quixote.get_response()
        
        the_int = int(request.form['special'])
        img = image.get_image(the_int)
        thumb = image.generate_thumbnail(img[0])
        response.set_content_type('image/png')
        
        return thumb
    
    @export(name='get_score')
    def get_score(self):
    	request = quixote.get_request()
    	response = quixote.get_response()
    	
    	the_int = int(request.form['special'])
    	score   = image.get_score(the_int)
    	return score
    
    @export(name='decrease_score')
    def decrease_score(self):
    	request = quixote.get_request()
    	response = quixote.get_response()
    	
    	try:
    		the_int = int(request.form['special'])
    	except:
    		the_int = -1
    		
    	image.decrease_score(the_int)
    
    @export(name='increase_score')
    def increase_score(self):
    	request = quixote.get_request()
    	response = quixote.get_response()
    	
    	try:
    		the_int = int(request.form['special'])
    	except:
    		the_int = -1
    	
    	
    	image.increase_score(the_int)