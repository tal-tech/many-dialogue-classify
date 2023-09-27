import time
import uuid

import flask

from sleepy_dog.c_config import Config
from sleepy_dog.c_data_backflow import send_data_flow
from sleepy_dog.c_eureka import eureka_register
from sleepy_dog.c_reqparser import Parser, type_url

if Config.DEPLOY_ENV != 'local':
    eureka_register()
url = type_url

app = flask.Flask(__name__)

parser = Parser()
parser.add_arguments("requestId", default=uuid.uuid4)
parser.add_arguments("timestamp", required=False)
parser.add_arguments("appKey", required=False)
# @arg_parse


@app.route('/', methods=["POST"])
def index():
    start_time = time.time()
    arg = parser.parse()
    response = {"code": 20000}

    send_data_flow(arg['requestId'], arg, response, start_time)
    return response


if __name__ == '__main__':
    app.run()
