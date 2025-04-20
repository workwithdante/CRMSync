""" from crmsync.api.WSClient import VTigerWSClient
from crmsync.config.config import SyncConfig

conf = SyncConfig()

client = VTigerWSClient(conf.host_api)
client.doLogin(conf.user_api, conf.token)
"""
 
from crmsync.api.ERPNextClient import ERPNextClient
from crmsync.config import SyncConfig

conf = SyncConfig()

client = ERPNextClient(conf.endpoint)
client.doLogin(conf.api_key, conf.api_secret)
