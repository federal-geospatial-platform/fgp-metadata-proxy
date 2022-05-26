from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

@app.route("/primary/catalogue/data.json")
def primary_server():
    with open ('./data/primary_server_data.json', encoding="utf8") as json_input:
        json_str = json_input.read()
    resp = Response(response=json_str,
                    status=200,
                    mimetype="application/json")

    return resp
    
@app.route("/secondary/catalogue")
def secondary_server():
    args = request.args
    if len(args) == 3 and \
       args["filter[owner]"] == "Manitoba_Government" and \
       "page[number]" in args and \
       "page[size]" in args:
        with open ('./data/secondary_server_data.json', encoding="utf8") as json_input:
            json_str = json_input.read()
        resp = Response(response=json_str,
                        status=200,
                        mimetype="application/json")
    else:
        resp = Response(response="Errorr: {}".format(str(args)),
                        status=400,
                        mimetype="text/plain")

    return resp

@app.route("/nl_geo_primary")
def nl_geo_primary_server():
    with open ('./data/NL/nl_geo_primary.html', encoding="utf8") as html_input:
        html_str = html_input.read()
    resp = Response(response=html_str,
                    status=200,
                    mimetype="text/html")

    return resp
    
@app.route("/nl_non_geo_primary")
def nl_non_geo_primary_server():
    with open ('./data/NL/nl_non_geo_primary.html', encoding="utf8") as html_input:
        html_str = html_input.read()
    resp = Response(response=html_str,
                    status=200,
                    mimetype="text/html")

    return resp
    
@app.route("/public/opendata/page/")
def nl_id_84():
    args = request.args
    if args["id"] in ["84", "741"]:
        file_name = './data/NL/nl_id_84.html'
    elif args["id"] in ["222", "421"]:
        file_name = './data/NL/nl_id_222.html'
    else:
        raise Exception ("invalid dataset id: {0}".format(args["id"]))
    with open (file_name, encoding="utf8") as html_input:
        html_str = html_input.read()
    resp = Response(response=html_str,
                    status=200,
                    mimetype="text/html")
    
    return resp
    
@app.route("/testing")
def testView1():
    ret = '{"OK"}'

    resp = Response(response=ret,
                    status=200,
                    mimetype="text/plain")

    return resp
    
    
@app.route("/valid_name")
def geoportal_weblink_adder():
    resp = Response(response="OK",
                    status=200,
                    mimetype="text/plain")

    return resp