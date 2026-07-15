import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery("placement_portal", broker=redis_url, include=["utils.tasks"])
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_ignore_result=True,
    broker_connection_retry_on_startup=False,
    broker_connection_retry=False,
    broker_transport_options={"socket_connect_timeout": 2, "socket_timeout": 2},
)
