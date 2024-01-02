import React, { useState } from 'react';
import axios from 'axios';

function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [signupSuccess, setSignupSuccess] = useState(false);
  const [signupError, setSignupError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Make an API request to the signup route of the Flask backend
    const data = { username, email, password };
    axios.post('/signup', data)
      .then((response) => {
        console.log(response.data.message);
        // Handle successful signup
        setSignupError('');
        setSignupSuccess(true);
        window.location.href = '/';
      })
      .catch((error) => {
        console.error(error);
        // Handle signup error
        setSignupError('An error occurred during signup. Please try again.');
        setSignupSuccess(false);
      });
  };

  return (
    <div>
      <h1>Sign Up</h1>
      {signupSuccess ? (
        <p>Sign up successful! Redirecting to another page...</p>
      ) : (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
      )}
    </div>
  );
}

export default SignUpPage;