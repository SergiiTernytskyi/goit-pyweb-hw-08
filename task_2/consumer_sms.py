import json
import os
import sys
import time

import pika
import connect

from models import Contact

SMS_QUEUE = "hw_8_sms_queue"


def update_contact_status(message):
    try:
        contact = Contact.objects(id__exact=message.get("id")).first()

        if contact:
            contact.update(sms_sent=True)
            print(f"Updated contact status for message: {message}")
        else:
            print(f"Contact with message '{message}' not found.")

    except Exception as e:
        print(f"Error updating contact status: {e}")


def send_sms(message):
    print(f"Simulating sending sms with message: {message}")

    update_contact_status(message)


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=SMS_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")

        time.sleep(2)
        send_sms(message)

        print(f" [x] Completed {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=SMS_QUEUE, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
