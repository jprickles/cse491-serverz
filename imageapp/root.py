import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        fileType = ( the_file.base_filename.split('.')[1] ).lower()
        if fileType == 'tiff' or fileType == 'tif':
        	fileType = 'tiff'
        elif fileType == 'jpeg' or fileType == 'jpg':
        	fileType = 'jpg'
        
        print 'received file of type: ' + fileType
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, fileType)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='list')
    def list(self):
    	templateVars = { "images" : image.images }
        return html.render('list.html', templateVars )

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        img = image.get_latest_image()
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
