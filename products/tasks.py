import time
import requests
from celery import shared_task
from django.conf import settings



@shared_task
def send_telegram(order_id, product_nomi, nechta, buyurtmachi_username, phone_number):
    time.sleep(5)
    token=settings.TELEGRAM_BOT_TOKEN
    method='sendMassege'
    message_text=f"New order: {order_id}\n  Product: {product_nomi}\n Nechta: {nechta}\n Klent: {buyurtmachi_username}\n tel: {phone_number}"

    response=requests.post(
        url=f"https//api.telegram.org/bot{token}/{method}",
        data={'chat_id': 5759797349, 'text': message_text}
    ).json()