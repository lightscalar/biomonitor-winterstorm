from vessel import Vessel
from glob import glob
import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from configure import *
from ipdb import set_trace as debug
from os.path import expanduser
import re


PORT = 5000
app = Flask(__name__)
CORS(app)
api = Api(app)

# Define valid SD cards.
valid_volumes = ['YELLOW', 'ORANGE', 'PINK', 'PURPLE', 'WHITE']
valid_volumes = ['/Volumes/{:s}'.format(v) for v in valid_volumes]


def get_board_name(volume_name):
    '''Extract the board name from the volume name.'''
    color = volume_name[9:]
    return 'bio_{:s}'.format(color.lower())


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


class Annotations(Resource):

    def get(self):
        # Index
        loc = expanduser('~')
        annotation_locs = '{:s}/Downloads/annotation*'.format(loc)
        available_files = glob(annotation_locs)
        return available_files


class Uploads(Resource):

    def post(self):
        # Try to upload data.
        data = request.json
        print(data)
        sd_card = data['volume']
        annotation_file = data['annotationFile']
        upload_data()
        board = get_board_name(sd_card)
        process_annotation(annotationFile, board_name)
        process_data()


class Configurations(Resource):

    def post(self):
        # Create a new data set.
        data = request.json
        configure_card(data)
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
api.add_resource(Annotations, '/annotations')
api.add_resource(Uploads, '/uploads')


if __name__ == '__main__':
    # app.run()
    wsgi.server(eventlet.listen(('localhost', PORT)), app)
