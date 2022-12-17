from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import func, text
from db import Session, CocktailRecipes, Ingredients, Base

app = Flask(__name__)
session = Session()

app = Flask(__name__)
CORS(app)

@app.route('/ingredients')
def ingredients():
    ingredients = session.query(Ingredients.ingredient_name, func.count(Ingredients.ingredient_name).label('count')).group_by(Ingredients.ingredient_name).order_by(text('count DESC'))
    return jsonify([i.ingredient_name for i in ingredients])

@app.route('/cocktails')
def cocktails():
    ingredients_list = request.args.getlist('ingredients')
    if not ingredients_list:
        return 'No ingredients provided', 400

    ingredients_list = ingredients_list[0].split(',')

    # get the number of ingredients for each cocktail that are not in the provided ingredients_list
    missing_counts = (session.query(Ingredients.cocktail_id, func.count(Ingredients.ingredient_name).label('missing_count'))
        .filter(~Ingredients.ingredient_name.in_(ingredients_list))
        .group_by(Ingredients.cocktail_id)
        .subquery())

    # get the total number of ingredients for each cocktail
    total_counts = (session.query(Ingredients.cocktail_id, func.count(Ingredients.ingredient_name).label('total_count'))
        .group_by(Ingredients.cocktail_id)
        .subquery())

    # join the missing and total counts with the cocktail_recipes table and order by the number of missing ingredients in the list
    cocktails = (session.query(CocktailRecipes, func.coalesce(missing_counts.c.missing_count, 0), func.coalesce(total_counts.c.total_count, 0))
                 .outerjoin(missing_counts, CocktailRecipes.id == missing_counts.c.cocktail_id)
                 .outerjoin(total_counts, CocktailRecipes.id == total_counts.c.cocktail_id)
                 .order_by(text('missing_count ASC'))
                 .with_entities(CocktailRecipes.name, CocktailRecipes.url, CocktailRecipes.rank, missing_counts.c.missing_count, total_counts.c.total_count)
            )

    # compute the required and available ingredients counts for each cocktail
    results = []
    for c in cocktails:
        required_count = c.total_count if c.total_count is not None else 0
        available_count = required_count - (c.missing_count if c.missing_count is not None else 0)
        results.append({'name': c.name, 'url': c.url, 'rank': c.rank, 'required_ingredients': required_count, 'available_ingredients': available_count})

    return jsonify(results)

if __name__ == '__main__':
    app.run()
