from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('postgresql://localhost:5432/postgres')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

class CocktailRecipes(Base):
    __tablename__ = 'cocktail_recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    rank = Column(Numeric(10, 2))

class Ingredients(Base):
    __tablename__ = 'ingredients'
    cocktail_id = Column(Integer, ForeignKey('cocktail_recipes.id'), primary_key=True)
    ingredient_name = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    cocktail = relationship('CocktailRecipes')
