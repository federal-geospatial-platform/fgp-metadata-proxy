from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

# Code for testing DCAT reader primary
@app.route("/primary/catalogue/data.json")
def primary_server():
    with open ('./data/primary_server_data.json', encoding="utf8") as json_input:
        json_str = json_input.read()
    resp = Response(response=json_str,
                    status=200,
                    mimetype="application/json")

    return resp
    
# Code for testing DCAT reader secondary
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

# Code for testing Socrata reader api/views
@app.route("/socrata/api/views")
def socrata_server_1():
    with open ('./data/socrata/api_views.json', encoding="utf8") as json_input:
        json_str = json_input.read()
    resp = Response(response=json_str,
                    status=200,
                    mimetype="application/json")

    return resp
    
# Code for testing Socrata reader api/views/3ctu-s8ip
@app.route("/socrata/api/views/3ctu-s8ip")
def socrata_server_2():
    with open ('./data/socrata/api_views_3ctu_s8ip.json', encoding="utf8") as json_input:
        json_str = json_input.read()
    resp = Response(response=json_str,
                    status=200,
                    mimetype="application/json")

    return resp
    
# Code for testing Socrata reader api/views/dq5v-qjry
@app.route("/socrata/api/views/dq5v-qjry")
def socrata_server_3():
    with open ('./data/socrata/api_views_dq5v_qjry.json', encoding="utf8") as json_input:
        json_str = json_input.read()
    resp = Response(response=json_str,
                    status=200,
                    mimetype="application/json")

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