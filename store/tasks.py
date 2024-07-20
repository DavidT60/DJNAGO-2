from time import sleep
from celery import shared_task

@shared_task
def send_emails_notification(messages=''):
    print("Sending Over 10k.. emeials")
    print(messages)
    sleep(10) # means 10 senconds....
    print("Action completed successfully...")
    