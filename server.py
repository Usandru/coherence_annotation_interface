from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import ast
import json
import random
import session

app = Flask(__name__)
api = Api(app)

CORS(app)

init = open('.\serv_data\init.cfg')
serverConfig = json.load(init)
init.close()

allSessions = {}

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class NewSession(Resource):
    def put(self):
        keywords = request.get_json()["session"].split("_")
        path = serverConfig[keywords[0]]
        mode = keywords[1]
        allSessions[serverConfig["id"]] = session.Session(serverConfig["id"], path, mode)
        return

class Annotate(Resource):
    def put(self):
        values = request.get_json()["annotation"]
        allSessions[serverConfig["id"]].writeToSessionLog(values)
        return

    def get(self):
        nextJSON = allSessions[serverConfig["id"]].getNextAnnotation()
        if nextJSON == None:
            serverConfig["id"] = serverConfig["id"] + 1
            init = open('.\serv_data\init.cfg', "w")
            json.dump(serverConfig, init)
            init.close()
            return jsonify({"LeftText": "Select annotation set", "RightText": "specify options", "InputMethod": "selector"})
        else:
            return jsonify(nextJSON)



api.add_resource(NewSession, '/session')
api.add_resource(Annotate, '/annotate')


if __name__ == '__main__':
     app.run(port=5002)