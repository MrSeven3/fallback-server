from flask import Flask

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>') #catch-all router
def catch_all(path):
    return 'You want path: %s' % path
