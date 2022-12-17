import React, { useState, useEffect } from 'react';
import { Table } from 'react-bootstrap';

export default function Cocktails({ ingredients = [] }) {
  const [cocktails, setCocktails] = useState([]);

  useEffect(() => {
    async function fetchCocktails() {
      const response = await fetch(`http://localhost:5000/cocktails?ingredients=${ingredients.join(',')}`);
      const data = await response.json();
      setCocktails(data);
    }
    fetchCocktails();
  }, [ingredients]);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Name</th>
          <th>URL</th>
          <th>Rank</th>
          <th>Ingredients</th>
        </tr>
      </thead>
      <tbody>
        {cocktails.map(({ name, url, rank, available_ingredients, required_ingredients }) => (
          <tr key={name}>
            <td>{name}</td>
            <td>
              <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
            </td>
            <td>{rank}</td>
            <td>{`${available_ingredients} / ${required_ingredients}`}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
