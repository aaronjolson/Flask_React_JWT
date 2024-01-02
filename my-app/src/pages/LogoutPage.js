import React, { useEffect } from 'react';

function LogoutPage() {

  useEffect(() => {
    // Clear the JWT token from local storage
    localStorage.removeItem('token');

    // Redirect the user back to the home page
    window.location.href = '/';
  }, []);

  return (
    <div>
      <h1>Logout</h1>
      <p>Logging out...</p>
    </div>
  );
}

export default LogoutPage;