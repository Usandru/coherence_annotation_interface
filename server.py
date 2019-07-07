from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import random
import session
import server_data as db_io

app = Flask(__name__)
api = Api(app)

CORS(app)

""" init = open('C:\data\serv_data\init.cfg')
serverConfig = json.load(init)
init.close()

allSessions = {} """

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

""" class NewSession(Resource):
    def put(self):
        keywords = request.get_json()["session"].split(" ")
        subset = keywords[0]
        interval_a = int(keywords[1])
        interval_b = int(keywords[2])
        mode = int(keywords[3])
        print(keywords)
        allSessions[serverConfig["id"]] = session.Session(serverConfig["id"], subset, interval_a, interval_b, mode)
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
            init = open('C:\data\serv_data\init.cfg', "w")
            json.dump(serverConfig, init)
            init.close()
            return jsonify({"LeftText": "", "RightText": "", "InputMethod": "selector"})
        else:
            return jsonify(nextJSON) """

class FetchSession(Resource):
    def get(self):
        identity = request.get_json()["ID"]
        return db_io.fetch_user(identity)

class ExtendSession(Resource):
    def put(self):
        identity = request.get_json()["ID"]
        db_io.extend_user(identity)
        return db_io.fetch_user(identity)

class ExtendUser(Resource):
    def put(self):
        params = request.get_json()
        identity = params["ID"]
        group = params["Group"]
        offset = params["Offset"]
        blocks = params["Blocks"]

        db_io.extend_user_with_params(identity, group, offset, blocks)
        return

class GenerateUser(Resource):
    def put(self):
        params = request.get_json()
        identity = params["ID"]
        group = params["Group"]
        offset = params["Offset"]
        blocks = params["Blocks"]

        db_io.generate_user(identity, group, offset, blocks)
        return

class GenerateUserDefault(Resource):
    def put(self):
        identity = request.get_json()["ID"]
        db_io.generate_user_default(identity)
        return db_io.fetch_user(identity)

class Annotate(Resource):
    def put(self):
        params = request.get_json()
        identity = params["ID"]
        content = params["Content"]
        db_io.annotate(identity, content)
        return

#api.add_resource(NewSession, '/session')
api.add_resource(Annotate, '/annotate')
api.add_resource(FetchSession, '/fetchsession')
api.add_resource(GenerateUser, '/generateuser')
api.add_resource(GenerateUserDefault, '/generateuserdefault')
api.add_resource(ExtendSession, '/extendsession')
api.add_resource(ExtendUser, '/extenduser')

if __name__ == '__main__':
     app.run(port=5002)
