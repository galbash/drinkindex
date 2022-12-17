from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

# Create the base class for our SQLAlchemy models
Base = declarative_base()

# Define the cocktail_recipes model
class CocktailRecipe(Base):
    __tablename__ = 'cocktail_recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    rank = Column(Numeric(10, 2))

# Define the ingredients model
class Ingredient(Base):
    __tablename__ = 'ingredients'
    cocktail_id = Column(Integer, ForeignKey('cocktail_recipes.id'), primary_key=True)
    ingredient_name = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    cocktail = relationship('CocktailRecipe')

# Connect to the database
engine = create_engine('postgresql://localhost:5432/postgres')

# Create the tables if they don't already exist
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


