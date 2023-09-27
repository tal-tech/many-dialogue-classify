import os
import logging


class Config:
    # @config
    API_TYPE = os.environ.get('API_TYPE') or '0'
    EUREKA_HOST_NAME = os.environ.get('EUREKA_HOST_NAME') or 'GODHAND-DIALOGUE-CLASSIFY'
    EUREKA_APP_NAME = os.environ.get('EUREKA_APP_NAME') or 'godhand-dialogue-classify'
    APOLLO_ID = os.environ.get('APOLLO_ID') or 'godhand-dialogue-classify'
    APOLLO_NAMESPACE = os.environ.get('APOLLO_NAMESPACE') or 'datawork-common'
    APP_URL = os.environ.get('APP_URL') or '/aitext/dialogue-classify'
    APOLLO_TOPIC = os.environ.get('APOLLO_TOPIC') or 'text'
    BIZ_TYPE = os.environ.get('BIZ_TYPE') or 'datawork-text'

    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
    TMP_FOLDER = os.path.join(BASE_FOLDER, 'temp')
    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)
    PORT = 5000

    DEPLOY_ENV = os.environ.get('DEPLOY_ENV') or 'local'
    APOLLO_URL = 'http://godhand-apollo-config:8080'
    if DEPLOY_ENV == 'local':
        EUREKA_URL = 'http://AILab:PaaS@eureka-dev.facethink.com/eureka/'
        DATA_CHANGE_URL = ''
        COUNT_URL = ""
    elif DEPLOY_ENV == "test":
        EUREKA_URL = 'http://AILab:PaaS@godhand-eureka:8761/eureka/'
        DATA_CHANGE_URL = 'http://internal.gateway-godeye-test.facethink.com/ossurl/material/ossconverts'
        COUNT_URL = "http://internal.gateway-godeye-test.facethink.com/stat/asyncApiCallback"
    elif DEPLOY_ENV == "pre":
        EUREKA_URL = 'http://AILab:PaaS@godhand-eureka-master:8761/eureka/,http://AILab:PaaS@godhand-eureka-slave1:8761/eureka/,http://AILab:PaaS@godhand-eureka-slave2:8761/eureka/'
        DATA_CHANGE_URL = 'http://internal.gateway.facethink.com/ossurl/material/ossconverts'
        COUNT_URL = "http://internal.gateway.facethink.com/stat/asyncApiCallback"
    elif DEPLOY_ENV == 'prod':
        EUREKA_URL = 'http://AILab:PaaS@godhand-eureka-master:8761/eureka/,http://AILab:PaaS@godhand-eureka-slave1:8761/eureka/,http://AILab:PaaS@godhand-eureka-slave2:8761/eureka/'
        DATA_CHANGE_URL = 'http://internal.openai.100tal.com/ossurl/material/ossconverts'
        COUNT_URL = "http://internal.openai.100tal.com/stat/asyncApiCallback"

    if os.environ.get('EUREKA_URL'):
        EUREKA_URL = os.environ.get('EUREKA_URL')
    if os.environ.get('APOLLO_URL'):
        APOLLO_URL = os.environ.get('APOLLO_URL')

    APOLLO_KAFKA = os.environ.get('APOLLO_KAFKA') or 'kafka-bootstrap-servers'
    VERSION = os.environ.get('VERSION') or '1.0'

    if os.environ.get('LOG_LEVEL') == 'INFO':
        LOG_LEVEL = logging.INFO
    else:
        LOG_LEVEL = logging.DEBUG

