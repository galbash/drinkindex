# DrinkIndex
> :warning: This README was auto-generated by ChatGPT, so it may contain errors. [Read more about that here](https://medium.com/@galbashan1/how-chatgpt-got-me-drunk-614d72d37f6f)

A tool to create an index of cocktails by scraping cocktail websites for cocktail recipes, parsing them using ChatGPT into ingredients and storing them in a searchable way, based on their ingredients.

# Features
* Scrape cocktail websites for cocktail recipes
* Parse cocktail recipes using ChatGPT into ingredients
* Store parsed ingredients in a searchable database
# Getting Started
1. Clone the repository and navigate to the project directory:
```
git clone https://github.com/username/DrinkIndex.git
cd DrinkIndex
```

2. Install dependencies for the crawler:
```
cd services/crawler
pip install -r requirements.txt
```
3. Start the crawler by running:
```
python crawler.py <crawl_root_url>
```
This will start crawling the given domain for cocktail recipes and output matches into a rabbitmq queue that the indexer will consume.

4. Install dependencies for the indexer:
```
cd ../indexer
pip install -r requirements.txt
```
5. Start the indexer by running:
```
python indexer.py
```
This will start consuming URLs from the rabbitmq queue and storing parsed ingredients in a local postgresql database.

6. Create the database tables by running the SQL script in the store directory:
```
cd ../store
psql < create_tables.sql
```
7. You can now search the database for cocktail ingredients.

# Contributing
We welcome contributions to DrinkIndex. To contribute, fork the repository and submit a pull request with your changes.

# License
DrinkIndex is released under the MIT License. See LICENSE for details.
