import hashlib
import os
import time

from flask import Flask, request, Response
from werkzeug.utils import secure_filename

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
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', TIME_FORMAT)


@app.route('/', methods=['GET'])
def ping():
    return 'ping successfully!'


@app.route('/1/<path:name>', methods=['get'])
def image(name):
    path = "uploads/%s" % name
    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp


@app.route('/qr/<name>', methods=['get'])
def qr(name):
    os.system('sh /root/python/pure_back_msg/cp.sh {}'.format(name))
    path = '/root/python/pure_back_msg/{}/main/QR.png'.format(name)
    while not os.path.exists(path):
        print('文件不存在 休眠1秒')
        time.sleep(1)
        break
    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp


@app.route('/pure/<name>', methods=['get'])
def pure(name):
    os.system('sh /root/python/pure_back_msg/cp.sh {}'.format(name))
    path = '/root/python/pure_back_msg/{}/main/QR.png'.format(name)
    while not os.path.exists(path):
        print('文件不存在 休眠1秒')
        time.sleep(1)
        break
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
    # secure_filename 处理文件名带 ././  的文件
    file_ext = os.path.splitext(secure_filename(file.filename))[-1]
    if file_ext not in ALLOWED_EXTENSIONS:
        return 'Unsupported file type', 415
    filename = '%s%s' % (str(md5.hexdigest()), file_ext)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not isPath(UPLOAD_FOLDER):
        createPath(UPLOAD_FOLDER)
    file.save(file_path)
    url = request.url.replace('/uploads', '/') + TIME_FORMAT + '/' + filename
    return url


@app.errorhandler(413)
def error(err):
    return '文件过大', 413


if __name__ == '__main__':
    app.run(host='0.0.0.0')
