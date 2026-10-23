import os
import urllib
from flask import Flask, request, render_template, Response
import datetime
import prometheus_client
from dotenv import load_dotenv
load_dotenv()

fallback_counter = prometheus_client.Counter("fallbacks_handled","The number of requests this fallback handler has handled, labeled by domain",["domain"])

app = Flask(__name__)

allowed_metrics_domain = os.environ.get("ALLOWED_PROMETHEUS_DOMAIN")

@app.before_request
def capture_fallback():
    url = urllib.parse.urlparse(request.base_url)
    print(f"{datetime.datetime.now(datetime.UTC)} | served domain {str(url.hostname)}, path was {str(url.path)}")

    fallback_counter.labels(domain=str(url.hostname)).inc()

@app.route("/metrics")
def show_metrics():
    url = urllib.parse.urlparse(request.base_url)

    if url.hostname == allowed_metrics_domain:
        return Response(prometheus_client.generate_latest(),mimetype=prometheus_client.CONTENT_TYPE_LATEST)
    else:
        return catch_all(url.path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>') #catch-all router
def catch_all(path):
    return render_template("index.html")
