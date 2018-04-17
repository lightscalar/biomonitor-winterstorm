from mathtools.utils import Vessel
from glob import glob
import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from configure import *
from ipdb import set_trace as debug


PORT = 5100
app = Flask(__name__)
CORS(app)
api = Api(app)

# Define valid SD cards.
valid_volumes = ['YELLOW', 'BLUE', 'RED', 'WHITE']
valid_volumes = ['/Volumes/{:s}'.format(v) for v in valid_volumes]


class Collections(Resource):

    def get(self):
        '''List available data collections.'''
        collections = glob('./data/arxiv/*.dat')
        payload = []
        for collection in collections:
            data = Vessel(collection)
            payload.append({'id': data.pid, 'duration': data.duration,
                'uploadedAt': data.uploaded_at})
        return payload


class Volumes(Resource):

    def get(self):
        # Index
        available = glob('/Volumes/*')
        valid = [v for v in available if v in valid_volumes]
        return valid


class Configurations(Resource):

    def post(self):
        # Create a new data set.
        data = request.json
        try:
            configure_card(data)
            status = 'OK'
        except:
            status = 'BAD'
        print(status)
        return {'sysStatus': status}


# ADD RESOURCE ROUTES.
api.add_resource(Volumes, '/volumes')
api.add_resource(Collections, '/collections')
api.add_resource(Configurations, '/configurations')


if __name__ == '__main__':
    app.run()
    # wsgi.server(eventlet.listen(('localhost', PORT)), app)
