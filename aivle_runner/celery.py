from celery import Celery
from . import config

app = Celery('aivle', include=['aivle_runner.tasks'])
app.config_from_object(config)
app.conf.broker_connection_retry_on_startup = True # Silence deprecation warning
