import urllib
from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>') #catch-all router
def catch_all(path):
    url = urllib.parse.urlparse(request.base_url)
    print(f"{datetime.datetime.now(datetime.UTC)} | served domain {str(url.hostname)}, path was {str(url.path)}")
    return 'You want path: %s' % path
