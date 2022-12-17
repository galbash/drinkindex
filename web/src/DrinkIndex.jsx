import React, { useState, useEffect } from 'react';
import Ingredients from './Ingredients';
import Cocktails from './Cocktails';

export default function DrinkIndex() {
  // Restore the saved selected ingredients when the component is first rendered
  const savedIngredients = JSON.parse(localStorage.getItem('selectedIngredients'));
  const [selectedIngredients, setSelectedIngredients] = useState(savedIngredients || []);
  const [showResults, setShowResults] = useState(false);

  // Save the selected ingredients to local storage when they change
  useEffect(() => {
    localStorage.setItem('selectedIngredients', JSON.stringify(selectedIngredients));
  }, [selectedIngredients]);

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

