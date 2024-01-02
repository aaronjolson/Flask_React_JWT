import logo from './logo.svg';
import './App.css';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import LoggedInIndicator from './components/LoggedInIndicator';

import SignUpPage from './pages/SignupPage';
import UploadPage from './pages/UploadPage';
import LoginPage from './pages/LoginPage';
import LogoutPage from './pages/LogoutPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import './Navigation.css';
import './LoggedInIndicator.css';

// Set the base URL for Axios requests
axios.defaults.baseURL = 'http://localhost:5000'; // Replace with the Flask server URL

export const UserContext = createContext();

export const useUserContext = () => useContext(UserContext);

function Navigation() {
  const location = useLocation();

  return (
    <nav>
      <ul className="navigation-list">
        <NavItem to="/" label="Home" current={location.pathname === '/home'} />
        <NavItem to="/signup" label="Sign Up" current={location.pathname === '/signup'} />
        <NavItem to="/login" label="Login" current={location.pathname === '/login'} />
        <NavItem to="/logout" label="Logout" current={location.pathname === '/logout'} />
        <NavItem to="/profile" label="Profile" current={location.pathname === '/profile'} />
      </ul>
    </nav>
  );
}

function NavItem({ to, label }) {
  const location = useLocation();

  // Conditionally hide the navigation item when on the corresponding page
  if (to === location.pathname) return null;

  return (
    <li className={`navigation-item ${location.pathname === to ? 'current' : ''}`}>
      <Link to={to}>{label}</Link>
    </li>
  );
}

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const authenticateUser = () => {
      // Retrieve the JWT token from storage (e.g., localStorage)
      const token = localStorage.getItem('token');

      // Check if the token exists and is valid
      if (token) {
        try {
          // Decode the JWT token
          const decodedToken = jwtDecode(token);
          // Update the user state with decoded information
          if (JSON.stringify(decodedToken) !== JSON.stringify(user)) {
            setUser(decodedToken);
          }
        } catch (error) {
          console.log('Invalid token:', error);
          setUser(null);
        }
      } else {
        setUser(null);
      }
    };

    authenticateUser();

    // Log the updated user state whenever it changes
  console.log(user);
  }, [user]);

  return (
    <UserContext.Provider value={user}>
      <Router>
        <div className="App">
          <Navigation />
          <LoggedInIndicator />

          <Routes>
            <Route path="/" element={<HomePage/>} />
            <Route path="/signup" exact element={<SignUpPage/>} />
            <Route path="/upload" element={<UploadPage/>} />
            <Route path="/login" element={<LoginPage/>} />
            <Route path="/logout" element={<LogoutPage/>} />
            <Route path="/profile" element={<ProfilePage/>} />
          </Routes>
        </div>
      </Router>
    </UserContext.Provider>
  );
}

export default App;
