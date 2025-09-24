---

```markdown
# Flask User Registration API

A simple Flask web application for user registration, using SQLite for storage and bcrypt for secure password hashing.  
Includes rate limiting and basic user validation.

## Features

- User registration (email, password, full name)
- Password strength & email validation
- Passwords are securely hashed
- SQLite database for persistent storage
- Rate limiting: 100 registrations per minute per IP
- Simple index page

## Requirements

- Python 3.7+
- pip

## Installation

1. **Clone the repository or download the files:**

    ```bash
    git clone https://github.com/lance-ui/Flask.git
    cd Flask
    ```

2. **Install dependencies:**

    ```bash
    pip install flask flask-limiter bcrypt
    ```

## Setup

No additional setup is required.  
The SQLite database (`database.db`) will be automatically created in your project directory when you run the app.

## Running the App

Start the Flask application:

```bash
python app.py
```

By default, the server runs on `http://0.0.0.0:5000/`.

## API Usage

### Register a New User

- **Endpoint:** `POST /api/v1/users/register`
- **Request Body (JSON):**
    - `email`: String (must be unique and valid)
    - `password`: String (minimum 8 characters, at least 1 number and 1 special character)
    - `fullName`: String

#### Example using `curl`:

```bash
curl -X POST http://localhost:5000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"MyPassw0rd!","fullName":"Test User"}'
```

#### Example success response:

```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### Example error response (duplicate email):

```json
{
  "message": "Email already exists"
}
```

## Testing

Use the curl example above or tools like Postman to test registration.

## Notes

- The registration endpoint is rate-limited (100 requests per minute per IP).
- Passwords are hashed using bcrypt before storing in the database.
- The index page (`/`) renders `index.html` if present. You can customize this template as needed.

## License

MIT
```

---