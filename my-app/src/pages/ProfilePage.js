import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useUserContext } from '../App';

function ProfilePage() {
  const [userInfo, setUserInfo] = useState(null);
  const user = useUserContext();

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        if (user && user.email) {
          const token = localStorage.getItem('token');
          const config = {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          };
          const response = await axios.get(`/user?email=${user.email}`, config);
          setUserInfo(response.data);
        }
      } catch (error) {
        console.log(error);
      }
    };

    fetchUserInfo();
  }, [user]);

  useEffect(() => {
    console.log(userInfo);
  }, [userInfo]);

  if (!user) {
    return (
        <div>
          <h1>You are not logged in!</h1>
          <p>Please sign up or Log in to continue...</p>

        </div>
    );
  }

  return (
    <div>
      <h1>Profile</h1>
      {userInfo ? (
        <div>
          <p>Username: {userInfo.userInfo.username}</p>
          <p>Email: {userInfo.userInfo.email}</p>
        </div>
      ) : (
        <p>Loading user info...</p>
      )}
    </div>
  );
}

export default ProfilePage;