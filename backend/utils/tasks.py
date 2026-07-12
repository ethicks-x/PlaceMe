from utils.celery_app import celery
from utils.notifications import send_chat_notification


@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def notify_chat_task(self, message):
    try:
        send_chat_notification(message)
    except Exception as exc:
        raise self.retry(exc=exc)
