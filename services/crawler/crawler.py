import pika
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlunparse

# Set up the connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queues
channel.queue_declare(queue='to_crawl')
channel.queue_declare(queue='drink_urls', durable=True)

# Parse the URL from the command line arguments
url = sys.argv[1]

# Parse the initial URL to extract the domain name
initial_url_parts = urlparse(url)
initial_domain = initial_url_parts.netloc

# Send the URL to the "to_crawl" queue
channel.basic_publish(exchange='', routing_key='to_crawl', body=url)
print('Sent URL to crawl: %s' % url)

# Define a callback function to process the URLs from the "to_crawl" queue
def crawl_url(ch, method, properties, body):
    # Get the page content
    page = requests.get(body)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Check if the page contains the required words
    if 'cocktail' in soup.text and 'recipe' in soup.text and 'ingredients' in soup.text:
        # Emit the URL to the "crawled" queue
        channel.basic_publish(exchange='', routing_key='drink_urls', body=body)
        print('Found cocktail recipe: %s' % body)

    # Find any additional URLs on the page
    for link in soup.find_all('a'):
        new_url = link.get('href')
        if new_url is not None and new_url.startswith('http'):
            # Parse the URL to extract the domain name
            url_parts = urlparse(new_url)
            new_domain = url_parts.netloc

            # Check if the new URL is on the same domain as the initial URL 
            if new_domain == initial_domain:
                # Check if the URL has already been crawled in the last two hours
                last_crawled = datetime.now() - timedelta(hours=2)
                if new_url not in crawled_urls or crawled_urls[new_url] < last_crawled:
                    # Parse the URL and remove the query parameters
                    query_params = parse_qs(url_parts.query)
                    url_parts = url_parts._replace(query='')
                    new_url_without_query = urlunparse(url_parts)

                    # Emit the new URL to the "to_crawl" queue
                    channel.basic_publish(exchange='', routing_key='to_crawl', body=new_url_without_query)
                    print('Added new URL to crawl: %s' % new_url_without_query)
                    crawled_urls[new_url_without_query] = datetime.now()

# Dictionary to store the URLs that have been crawled
crawled_urls = {}

# Consume the URLs from the "to_crawl" queue
channel.basic_consume(queue='to_crawl', on_message_callback=crawl_url, auto_ack=True)
print('Waiting for URLs to crawl. To exit press CTRL+C')
channel.start_consuming()

