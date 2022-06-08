import flask
import sys
import jsonpickle
import json
import threading
import socket
import config
import werkzeug.utils
from pdf_reader_service import PdfReaderService
from flask_cors import CORS, cross_origin


def jsonify(o):
    js = jsonpickle.dumps(o, False)
    dico = json.loads(js)
    return flask.jsonify(dico)

app: flask.Flask = flask.Flask(__name__)
cors = CORS(app)


@app.route("/", methods=['GET'])
def autodoc():
    s = f"<html><body><h1>NP Rest V{config.version}</h1>"
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    s += f"<p>{host}@{ip}:5000</p>"
    l = list(app.url_map.iter_rules())
    l.sort(key=lambda x: x.rule)
    for rule in l:
        s += f"{rule.methods} <a href='http://{ip}:5000{rule.rule}'>{rule.rule.replace('<','&lt;').replace('>','&gt;')}</a><br/>"
    s += "</body></html>"
    return s


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/version", methods=['GET'])
def version():
    return str(config.version)


@app.route('/upload', methods = ['POST'])
@cross_origin()
def uploader():
    print("Upload")
    files = flask.request.files.getlist("file[]")
    res = []
    for f in files:
        file = f"docs/{werkzeug.utils.secure_filename(f.filename)}"
        f.save(file)
        print(f"{file} uploaded successfully")
        service = PdfReaderService(file)
        service.parse()
        service.matches()
        d = {"prices": service.get_best(), "account": service.get_account()}
        print(d)
        res.append(d)
    return json.dumps(res)

if __name__ == '__main__':
    print("FactureX API")
    print("============")
    print(f"V{config.version}")
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    lock = threading.RLock()
    app.run(host='0.0.0.0', threaded=True, debug=True, use_reloader=False)
