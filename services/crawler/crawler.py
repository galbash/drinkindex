import pika


# connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

# create a queue to publish messages to, if it does not already exist
channel.queue_declare(queue='drink_urls', durable=True)

# publish a message to the queue
channel.basic_publish(
    exchange='',
    routing_key='drink_urls',
    body='Hello from the crawler!')

# close the connection
connection.close()

