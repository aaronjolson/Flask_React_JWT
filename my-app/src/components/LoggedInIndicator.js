import React from 'react';
import { useUserContext } from '../App';

function LoggedInIndicator() {
  const user = useUserContext();

  return (
    <div className="login-indicator">{user ? '✔️' : '❌'}</div>
  );
}

export default LoggedInIndicator;