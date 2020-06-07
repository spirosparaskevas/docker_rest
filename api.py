from flask import Flask, jsonify
from flask_restful import Resource, Api
import docker

app = Flask(__name__)
api = Api(app)
client = docker.from_env()
container_name = 'dash_app'


class IndexPage(Resource):
    def get(self):
        return jsonify({'start_container': '/start',
                        'status_container': '/status',
                        'stop_container': '/stop', })


class DockerStart(Resource):
    def get(self):
        try:
            dash_container = client.containers.run(
                'dash', ports={'8050': '8050'}, name=container_name, detach=True, remove=True)
            return jsonify({'status': dash_container.status, })
        except docker.errors.APIError as e:
            return jsonify({'error': e.explanation})


class DockerStatus(Resource):

    def get(self):
        try:
            dash_container = client.containers.get(container_name)
            return jsonify({'status': dash_container.status,
                            'url': '46.101.248.180:8050'})
        except docker.errors.NotFound as e:
            return jsonify({'error': e.explanation})


class DockerStop(Resource):
    def get(self):
        try:
            dash_container = client.containers.get(container_name)
            dash_container.stop()
            return jsonify({'stoped': True})
        except docker.errors.APIError as e:
            return jsonify({'error': e.explanation})
        except docker.errors.NotFound as e:
            return jsonify({'error': e.explanation})


api.add_resource(IndexPage, '/')
api.add_resource(DockerStart, '/start')
api.add_resource(DockerStatus, '/status')
api.add_resource(DockerStop, '/stop')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
