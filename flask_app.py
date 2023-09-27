import time
import uuid

import flask
from flask import request

from sleepy_dog.c_config import Config
from sleepy_dog.c_data_backflow import send_data_flow
from sleepy_dog.c_eureka import eureka_register
from sleepy_dog.c_reqparser import Parser, TypeText
from sleepy_dog.logger import g_logger
from sleepy_dog.utility import make_response
from sleepy_dog.exception import Const, EvaEx
from src.main import classfier

if Config.DEPLOY_ENV != 'local':
    eureka_register()

app = flask.Flask(__name__)

parser = Parser()
parser.add_arguments("requestId", default=uuid.uuid4)
parser.add_arguments("timestamp", required=False)
parser.add_arguments("appKey", required=False)
parser.add_arguments('text', required=True, type=TypeText)


@app.route('/', methods=["POST"])
def index():
    start_time = time.time()
    arg = parser.parse()
    # g_logger.debug(f'headers: {request.headers}, arg:{arg}')
    try:
        ret = classfier.classify(arg['text'])
        if ret.get("code") != 0:
            g_logger.error(f"{arg['requestId']} return error: {ret}")
            raise EvaEx("algorithm error")
        response = make_response(Const.SUCCESS, arg['requestId'], dict(result=ret['data']))
    except Exception as e:
        g_logger.error(f"{arg['requestId']} internal error: {e}, ret:{arg['text']}")
        response = make_response(Const.INTERNAL_ERR, arg['requestId'])
    send_data_flow(arg['requestId'], arg, response.json, start_time)
    return response


@app.route("/status/readiness")
def status():
    return "good"


if __name__ == '__main__':
    app.run()
