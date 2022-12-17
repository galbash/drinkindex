import React, { useState, useEffect } from 'react';

export default function Ingredients({ selectedIngredients, onChange }) {
  const [ingredients, setIngredients] = useState([]);

  useEffect(() => {
    async function fetchIngredients() {
      const response = await fetch('http://localhost:5000/ingredients');
      const data = await response.json();
      setIngredients(data);
    }
    fetchIngredients();
  }, []);
  const handleChange = (event) => {
    const { name } = event.target;
    if (selectedIngredients.includes(name)) {
      // remove the ingredient from the array
      const updatedIngredients = selectedIngredients.filter(ingredient => ingredient !== name);
      onChange(updatedIngredients);
    } else {
      // add the ingredient to the array
      const updatedIngredients = [...selectedIngredients, name];
      onChange(updatedIngredients);
    }
  };

  return (
    <ul>
      {ingredients.map((ingredient) => (
        <li key={ingredient}>
          <label>
            <input
              type="checkbox"
              name={ingredient}
              checked={selectedIngredients.includes(ingredient)}
              onChange={handleChange}
            />
            {ingredient}
          </label>
        </li>
      ))}
    </ul>
  );
}
