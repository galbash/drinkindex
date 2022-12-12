import pika
import time
import sys
import requests
from bs4 import BeautifulSoup
from revChatGPT.revChatGPT import Chatbot
from db import CocktailRecipe, Ingredient, session
import traceback

print(sys.argv)
config = {
    #"email": sys.argv[1],
    #"password": sys.argv[2],
    "session_token": sys.argv[1],
    "cf_clearance": sys.argv[2],
    "user_agent": sys.argv[3]
}

chatbot = Chatbot(config, conversation_id=None)

# connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue to consume messages from, if it does not already exist
channel.queue_declare(queue='drink_urls', durable=True)

QUESTION = """From the following text below, please understand if it is an article describing a cocktail recepie. If it is, output the following: The first line should be: "<cocktail name>: <ranking>". If the ranking doesn't exist output "-". use only lowercase letters and the generic name of the cocktail, without mentioning brands. the following lines contain the ingredients: each line should contain one ingredient and it's amount in the format "<ingredient>: <amount>". The ingredient part (before the semicolon) should contain only the ingredient name, not the amount. If it is not a cocktail recepie, output only the word "no". Output the ingredients in their generic name, and don't include a brand. For example, instead of "bacardi white rum" output "white rum". All of the output should be lower cased, don't capitalize any word. The text is: %s"""

# define a callback function to process incoming messages
def process_message(ch, method, properties, body):
    time.sleep(5)
    try:
        print(body)
        page = requests.get(body)
        soup = BeautifulSoup(page.content, "html.parser")
        
        response = chatbot.get_chat_response(QUESTION % soup.text, output="text")['message']
        if response == "no":
            print("not a cocktail")
            return
        print(response)

        lines = response.split('\n')
        name, rank = lines[0].split(':')
        name = name.strip()
        try:
            rank = float(rank.strip())
        except:
            rank = None
        
        ingredients = [line.split(':') for line in lines[1:] if ':' in line]
        ingredients = [(ingredient.strip(), amount.strip()) for ingredient, amount in ingredients]

        # Insert the cocktail into the cocktail_recipes table
        cocktail = CocktailRecipe(name=name, url=body, rank=rank)
        session.add(cocktail)
        session.commit()
        
        # Insert the ingredients into the ingredients table
        for ingredient, amount in ingredients:
            ingredient = Ingredient(cocktail_id=cocktail.id, ingredient_name=ingredient, amount=amount)
            session.add(ingredient)
        
        session.commit()
    except Exception:
        session.rollback()
        print(traceback.format_exc())

# consume messages from the queue, using the callback function to process them
channel.basic_consume(queue='drink_urls', on_message_callback=process_message, auto_ack=True)

# start consuming messages
channel.start_consuming()
