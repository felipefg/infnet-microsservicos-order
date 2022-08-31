import pika

from orders import Order

ON_ORDER_CREATED = "orderCreated"


def connect():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(ON_ORDER_CREATED)

    return connection, channel


CONNECTION, CHANNEL = connect()


def emit_order_created(order: Order):
    CHANNEL.basic_publish(
        exchange='',
        routing_key=ON_ORDER_CREATED,
        body=order.json()
    )
