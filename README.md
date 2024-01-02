# Flask React JWT Complete Demo
Introducing an innovative, full-stack web development project engineered to expedite and enrich your coding journey! 
This project is a powerhouse starting point, perfect for educational environments 
or as the foundation for your next groundbreaking web application. 
Built with the latest industry standards, this project boasts secure and robust authentication mechanisms 
using best-practice password hashing techniques and JWT (JSON Web Tokens) for seamless session management.

The Project utilizes Flask, a highly flexible and efficient backend framework, integrated with Postgres - the powerful, open-source relational database. 
The frontend utilizes React, the cutting-edge framework renowned for its incredible efficiency and the ability to craft dynamic user interfaces.

Key features that make up this project include:
- A streamlined signup form, welcoming new users to the platform.
- A secure login form, incorporating advanced encryption.
- A simple logout page, ensuring users can easily exit the system and have their data reliably cleared.
- An exclusive profile page, meticulously safeguarded, only accessible post-authentication,
demonstrating how to add an extra layer of validation for a secure user experience.
- A playground to explore the interactions between the backend, the database, and the frontend in a realistic 
but not overly complicated system.

Ease-of-use and cross a platform compatibility is made possible through full deployability via Docker Compose, 
streamlining the launch process and ensuring consistency across various environments. 
Whether you are an educator seeking a comprehensive tool for instructing aspiring developers, or 
an innovator needing a reliable base to craft your next digital venture, 
this project is your gateway to harnessing the full potential of modern web technologies.
Unlock the power of full-stack web development today and propel your projects into the future!

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
   git clone https://github.com/aaronjolson/Flask_React_JWT.git
   
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

6. Navigate to localhost:5000 and explore.

## Debugging and development
### Stopping the application
To stop the application and remove the containers, run the following command:
   ```shell
   docker-compose down
  ```

## Contributing
Feel free to contribute to this repository by submitting a pull request or opening an issue.
