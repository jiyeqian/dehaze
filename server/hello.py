#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

from dehaze.dehaze import dehaze

UPLOAD_FOLDER = './static/origin'
RESULT_FOLDER = './static/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])

filenames = ['./static/origin/demo.jpg',
             './static/result/demo_dark.jpg',
             './static/result/demo_rawt.jpg',
             './static/result/demo_refinedt.jpg',
             './static/result/demo_rawrad.jpg',
             './static/result/demo_rerad.jpg']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def filename_suffix(filename, suffix):
    strs = filename.rsplit('.', 1)
    filename = strs[0] + '_' + suffix + '.' + strs[1]
    return os.path.join(app.config['RESULT_FOLDER'], filename)


def generate_result_filenames(filename):
    filenames = []
    filenames.append(filename_suffix(filename, 'dark'))
    filenames.append(filename_suffix(filename, 'rawt'))
    filenames.append(filename_suffix(filename, 'refinedt'))
    filenames.append(filename_suffix(filename, 'rawrad'))
    filenames.append(filename_suffix(filename, 'rerad'))
    return filenames


def resize_image(im):
    wide = im.size[0]
    if im.size[1] > wide:
        wide = im.size[1]
    if wide > 400:
        ratio = 400. / wide
        im = im.resize((int(im.size[0] * ratio), int(im.size[1] * ratio)))
    return im


def image_dehaze(filename):
    from PIL import Image
    path_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filenames = generate_result_filenames(filename)
    im = Image.open(path_filename)
    im = resize_image(im)
    im.save(path_filename)
    dark, rawt, refinedt, rawrad, rerad = dehaze(im)
    dark.save(filenames[0])
    rawt.save(filenames[1])
    refinedt.save(filenames[2])
    rawrad.save(filenames[3])
    rerad.save(filenames[4])
    return filenames


@app.route('/dehaze', methods=['GET', 'POST'])
def upload_file():
    global filenames
    # filenames = ['./static/result/demo_dark.jpg',
    #              './static/result/demo_rawt.jpg',
    #              './static/result/demo_refinedt.jpg',
    #              './static/result/demo_rawrad.jpg',
    #              './static/result/demo_rerad.jpg']
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename.lower() in ALLOWED_EXTENSIONS:
                today = datetime.today()
                filename = today.strftime("%Y%m%d%H%S_") + \
                           str(today.microsecond) + '.' + filename
            origin_file = os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename)
            file.save(origin_file)
            filenames = image_dehaze(filename)
            filenames.insert(0, origin_file)
            # print filenames
            return redirect(url_for('upload_file',
                                    filenames=filenames))
    # print filenames
    return render_template('index.html', filenames=filenames)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''

if __name__ == '__main__':
    app.run(debug=True)
