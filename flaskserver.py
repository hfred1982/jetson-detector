from flask import Flask, json, request

config = {'status' : 'No network started yet'}

api = Flask(__name__)

@api.route('/config', methods=['GET'])
def get_config():
  return json.dumps(config)


@api.route('/config', methods=['POST'])
def post_config():
    global config
    config = request.json
    return json.dumps({"success": True}), 201


if __name__ == '__main__':
    api.run(host='0.0.0.0')