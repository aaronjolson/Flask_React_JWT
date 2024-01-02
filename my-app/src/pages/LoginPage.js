import React, { useState } from 'react';
import axios from 'axios';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('/login', { email, password });
      const token = response.data.token;
      // Store the token in browser storage or state
      localStorage.setItem('token', token);
      // TODO: Redirect to another page or perform other actions after successful login
      // Example: Redirect to the main page
      window.location.href = '/';
    } catch (error) {
      console.error(error);
      setLoginError('Invalid email or password');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleLogin();
  };

  return (
    <div>
      <h1>Login</h1>
      {loginError && <p className="error">{loginError}</p>}
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;