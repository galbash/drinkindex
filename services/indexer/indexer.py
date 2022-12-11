import pika

# connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue to consume messages from, if it does not already exist
channel.queue_declare(queue='drink_urls', durable=True)

# define a callback function to process incoming messages
def process_message(ch, method, properties, body):
    print('Received message:', body)

# consume messages from the queue, using the callback function to process them
channel.basic_consume(queue='drink_urls', on_message_callback=process_message, auto_ack=True)

# start consuming messages
channel.start_consuming()
