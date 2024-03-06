
# Flask API Documentation
This is a Flask-based RESTful API for managing users. It provides endpoints for user authentication, user registration, updating user details, and retrieving user information.






## Installation
To run this application locally, follow these steps:

```bash
  git clone https://github.com/faruk005/injozi.git
```

Go to the project directory

```bash
  cd injozi
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set up environment variables:
Create a .env file in the root directory and add the following variables:

```
    MONGO_URI=<your-mongodb-uri>
    SECRET_KEY=<your-secret-key>
```

Start the server

```bash
  python app.py
```

The API server will start running at http://localhost:5000.
## API Reference

#### Authentication

```http
  GET /
```

| Method | Url     | Description                |
| :-------- | :------- | :------------------------- |
| `POST` | `/auth/signup` | **Required**. Register a new user. Requires name, email, password, role, and phone fields in the request body. |
| `POST` | `/auth/login` | Authenticate and log in a user. Requires email and password fields in the request body. |
| `GET` | `/user/me` | **Required:** token. Get current user details. Requires authentication.|
| `PUT` | `/user/me` | **Required** token. Update user details. Requires authentication. Allows updating name and phone fields. |
| `GET` | `/user/all` | **Required** token. Get details of all users. Requires superadmin role. |

### Headers
#### Authorization
Bearer Token

