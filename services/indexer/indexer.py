import pika
import sys
import requests
from bs4 import BeautifulSoup
from revChatGPT.revChatGPT import Chatbot

config = {
    "session_token": sys.argv[1],
}

chatbot = Chatbot(config, conversation_id=None)

# connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue to consume messages from, if it does not already exist
channel.queue_declare(queue='drink_urls', durable=True)

QUESTION = """From the following text below, please understand if it is an article describing a cocktail recepie. If it is, output only a list of ingrediants in the following format: each line should contain one ingredient and it's amount in the format "<ingredient>: <amount>". If it is not a cocktail recepie, output only the word "no". Output the ingredients in their generic name, and don't include a brand. For example, instead of "bacardi white rum" output "white rum". All of the output should be lower cased, don't capitalize any word. The text is: %s"""

# define a callback function to process incoming messages
def process_message(ch, method, properties, body):
    print(body)
    page = requests.get(body)
    soup = BeautifulSoup(page.content, "html.parser")
    
    response = chatbot.get_chat_response(QUESTION % soup.text, output="text")
    if response == "no":
        return
    print(response)


# consume messages from the queue, using the callback function to process them
channel.basic_consume(queue='drink_urls', on_message_callback=process_message, auto_ack=True)

# start consuming messages
channel.start_consuming()
