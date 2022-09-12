import pika

from orders import Order

EXCHANGE_NAME = "FTGO"

SERVICE_NAME = "order"

# Event Types
ORDER_CREATED = "orderCreated"
ORDER_CANCELLED = "orderCancelled"


def connect():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")

    return connection, channel


CONNECTION, CHANNEL = connect()


def emit_order_created(order: Order):
    CHANNEL.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=f'{SERVICE_NAME}.{ORDER_CREATED}',
        body=order.json()
    )


def emit_order_cancelled(order: Order):
    CHANNEL.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=f'{SERVICE_NAME}.{ORDER_CANCELLED}',
        body=order.json()
    )
