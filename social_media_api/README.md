# Social Media API

## Project Overview
This is a Django-based Social Media API with user authentication and profile management.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/accounts/register/`: User registration
- `POST /api/accounts/login/`: User login
- `GET /api/accounts/profile/`: Retrieve user profile (requires token)
- `PUT /api/accounts/profile/`: Update user profile (requires token)

### Authentication Flow
1. Register a new user
2. Receive an authentication token
3. Use the token in the `Authorization` header for subsequent requests
   - Header format: `Authorization: Token <your_token_here>`

## User Model
Custom user model with additional fields:
- username
- email
- bio
- profile_picture
- followers
- following

## Testing
Use tools like Postman or curl to test the API endpoints.

## Security
- Token-based authentication
- Password hashing
- User registration validation
