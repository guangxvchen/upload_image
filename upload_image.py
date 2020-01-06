import hashlib
import os
import time

from flask import Flask, request, Response

from utils.utils_file import isPath, createPath
from utils.utils_time import timeFormat

md5 = hashlib.md5()
app = Flask(__name__)
# 文件大小 5M
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = set(
    ['.bmp', '.jpg', '.png', '.tif', '.gif', '.pcx', '.tga', '.exif', '.fpx', '.svg', '.psd', '.cdr', '.pcd', '.dxf',
     '.ufo', '.eps', '.ai', '.raw', '.WMF', '.webp'])
TIME_FORMAT = timeFormat('%Y%m%d')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads\\', TIME_FORMAT)


@app.route('/ping', methods=['GET'])
def ping():
    return 'ping successfully!'


@app.route('/<path:name>', methods=['get'])
def image(name):
    path = "uploads/%s" % name
    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp


@app.route('/uploads', methods=['POST'])
def uploads():
    md5.update(str(time.time()).encode(encoding='utf-8'))
    # file 为文件的名称
    if 'file' not in request.files:
        print('no photo detected')
        return 'No file detected', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_ext = os.path.splitext(file.filename)[-1]
    if file_ext not in ALLOWED_EXTENSIONS:
        return 'Unsupported file type', 415
    filename = '%s%s' % (str(md5.hexdigest()), file_ext)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not isPath(UPLOAD_FOLDER):
        createPath(UPLOAD_FOLDER)
    file.save(file_path)
    url = request.url.replace('/uploads', '/') + TIME_FORMAT + '/' + filename
    return url


if __name__ == '__main__':
    app.run()
