import React from 'react';
import { useUserContext } from '../App';

function HomePage() {
  const user = useUserContext();

  return (
    <div>
      <h1>Home</h1>
      {user ? (
        <p>Hello, {user.email}</p>
      ) : (
        <p>Hello stranger, please sign up or sign in</p>
      )}
    </div>
  );
}

export default HomePage;