from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed, TEXT

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
docs = UploadSet('docs', TEXT)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOADED_PHOTOS_ALLOW'] = ['txt', 'py']
#app.config['UPLOADED_PHOTOS_DENY'] = ['jpg']
app.config['UPLOADS_DEFAULT_DEST'] = 'other'

configure_uploads(app, (photos, docs))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'thefile' in request.files:
        try:
            doc_filename = docs.save(request.files['thefile'])
            #return '<h1>+photos.path(image_filename)+</h1>'
            return '<h1>+docs.url(doc_filename)+</h1>'
        except UploadNotAllowed:
            return '<h1>Not allowed file format.</h1>'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)