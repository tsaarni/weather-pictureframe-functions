#!/usr/bin/env python3

import io
from flask import send_file
from PIL import Image
from display import Display


def image_get2(req):
    image = Image.new('1', (400, 300), 'white')
    d = Display(image)
    d.draw()
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype='image/png', cache_timeout=60*10)


# for testing locally
if __name__ == '__main__':
    from flask import Flask, request
    import os
    app = Flask(__name__)

    with open('.env.yaml') as env:
        for line in env.readlines():
            key, val = line.split(':')
            os.environ[key] = val.strip()

    @app.route('/image')
    def index():
        return image_get2(request)

    app.run(host='0.0.0.0', port=8080, debug=True)
