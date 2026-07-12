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
    # Fire-and-forget: nothing ever calls .get() on these tasks, so skip
    # the result backend entirely - no need to write/track task state.
    task_ignore_result=True,
    # If Redis is unreachable, fail fast instead of retrying with backoff -
    # a request enqueueing a notification should never hang on this.
    broker_connection_retry_on_startup=False,
    broker_connection_retry=False,
    broker_transport_options={"socket_connect_timeout": 2, "socket_timeout": 2},
)
