-- Create the table for cocktail recipes
CREATE TABLE cocktail_recipes (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  url VARCHAR(255) NOT NULL,
  rank NUMERIC(10, 2)
);

-- Create the table for ingredients
CREATE TABLE ingredients (
  cocktail_id INTEGER NOT NULL,
  ingredient_name VARCHAR(255) NOT NULL,
  amount VARCHAR(255) NOT NULL,
  PRIMARY KEY (cocktail_id, ingredient_name),
  FOREIGN KEY (cocktail_id) REFERENCES cocktail_recipes(id)
);

