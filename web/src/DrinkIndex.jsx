import React, { useState, useEffect } from 'react';
import Ingredients from './Ingredients';
import Cocktails from './Cocktails';

export default function DrinkIndex() {
  const [showResults, setShowResults] = useState(false);
  const [selectedIngredients, setSelectedIngredients] = useState([]);

  // Save the selected ingredients to local storage when they change
  useEffect(() => {
    localStorage.setItem('selectedIngredients', JSON.stringify(selectedIngredients));
  }, [selectedIngredients]);

  // Restore the saved selected ingredients when the component is first rendered
  useEffect(() => {
    const savedIngredients = JSON.parse(localStorage.getItem('selectedIngredients'));
    if (savedIngredients) {
      setSelectedIngredients(savedIngredients);
    }
  }, []);

  const handleSearch = () => {
    setShowResults(true);
  };

  return (
    <div>
      {!showResults && (
        <>
          <h1>Select ingredients</h1>
          <Ingredients
            selectedIngredients={selectedIngredients}
            onChange={setSelectedIngredients}
          />
          <button onClick={handleSearch}>Search</button>
        </>
      )}
      {showResults && (
        <>
          <h1>Cocktail recipes</h1>
          <Cocktails ingredients={selectedIngredients} />
        </>
      )}
    </div>
  );
}
