# Flask React JWT Complete Demo
This project is intended to be used as a starting point and teaching tool for building web projects that
have a self-managed login, (hashed) password storage, JWT tokens for auth and session management, 
Flask as the backend framework connected to Postgres, and React as the frontend framework.   

The app's main features include
- A signup form
- A login form
- A logout form
- A protected profile page that can only be accessed by a user that has successfully signed up and logged in
 
It is fully deployable using Docker Compose.

## Prerequisites
- Docker 
- Docker Compose
- NodeJS
- npm
- React
- Python 3.8+


## Getting Started

1. Clone the repository:

   ```shell
   git clone <repository-url>
   
2. cd into project
   ```shell
   cd Flask_React_JWT

3. Build and start the containers using Docker Compose
   ```shell
   docker-compose up -d

4. Initialize the DB
   ```shell
    python init_db.py

5. Run the Frontend
   ```shell 
   cd my-app
   npm install
   npm start
   ```

## Debugging and development
### Stopping the application
To stop the application and remove the containers, run the following command:
   ```shell
   docker-compose down
  ```

## Contributing
Feel free to contribute to this repository by submitting a pull request or opening an issue.
