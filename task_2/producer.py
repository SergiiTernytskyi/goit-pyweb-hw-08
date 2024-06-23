import pika
import json
from faker import Faker
from models import Contact
import connect


fake = Faker("uk-Ua")
NUMBER_OF_CONTACTS = 10
EMAIL_QUEUE = "hw_8_email_queue"
SMS_QUEUE = "hw_8_sms_queue"


def create_contact():
    contact = Contact(
        fullname=fake.full_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        send_method=fake.random_element(elements=("email", "sms")),
    )

    contact.save()
    return contact


def sent_to_queue(queue_type, message):
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="Homework-8 exchange", exchange_type="direct")
    channel.queue_declare(queue=queue_type, durable=True)
    channel.queue_bind(exchange="Homework-8 exchange", queue=queue_type)
    channel.basic_publish(
        exchange="Homework-8 exchange",
        routing_key=queue_type,
        body=message.encode(),
    )
    connection.close()


def main():
    for _ in range(NUMBER_OF_CONTACTS):
        contact = create_contact()

        if contact:
            message = json.dumps(
                {"id": str(contact.id), "payload": str(contact.fullname)}
            )

            if contact.send_method == "email":
                sent_to_queue(EMAIL_QUEUE, message)
            elif contact.send_method == "sms":
                sent_to_queue(SMS_QUEUE, message)


if __name__ == "__main__":
    main()
