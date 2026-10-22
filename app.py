import urllib
from flask import Flask, request, render_template
import datetime
import prometheus_client

fallback_counter = prometheus_client.Counter("fallbacks_handled","The number of requests this fallback handler has handled, labeled by domain",["domain"])
prometheus_client.start_http_server(8000)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>') #catch-all router
def catch_all(path):
    url = urllib.parse.urlparse(request.base_url)
    print(f"{datetime.datetime.now(datetime.UTC)} | served domain {str(url.hostname)}, path was {str(url.path)}")

    fallback_counter.labels(domain=str(url.hostname)).inc()

    return render_template("index.html")
