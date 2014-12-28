from ConfigModule import Config
from AvocadoAPIModule import AvocadoAPI
from AvocadoAPIModule import AuthClient
import logging

logging.basicConfig(level=logging.DEBUG)
configuration = Config("config.ini")
avocado_user_agent = configuration.get('Avocado Requests', 'Avocado User Agent')

api = AvocadoAPI(configuration, avocado_user_agent, AuthClient(configuration, avocado_user_agent))
api.authenticate()
api.test_api_communication()