from crmsync.api.WSClient import VTigerWSClient
from crmsync.config.config import SyncConfig

conf = SyncConfig()

client = VTigerWSClient(conf.host_api)
client.doLogin(conf.user_api, conf.token)
