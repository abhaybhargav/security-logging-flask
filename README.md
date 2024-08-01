# Secure Flask App with Security Logging

This project demonstrates a simple Flask application with security logging features. It includes user authentication, credit card management, and comprehensive security logging.

## Features

- User signup and login
- Credit card creation and viewing
- Security logging for various events
- SQLite database for data storage
- Bootstrap for consistent UI design
- Dockerized application

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd secure_flask_app
   ```

2. Build the Docker image:
   ```
   docker build -t secure-flask-app .
   ```

3. Run the container:
   ```
   docker run -p 8880:8880 secure-flask-app
   ```

The application will be accessible at `http://localhost:8880`.

## How the App Works

The app consists of several main components:

1. **User Authentication**: Users can sign up and log in. Passwords are hashed before storage.
2. **Credit Card Management**: Logged-in users can create and view credit cards.
3. **Security Logging**: The app logs various security-related events to a file.

## Operating the App and Triggering Security Logs

### 1. Signup Input Validation Violation

- Navigate to the signup page (`/signup`).
- Try to create an account with a username less than 3 characters or a password less than 8 characters.
- This will trigger a log entry for signup input validation violation.

### 2. Authentication Failure

- Go to the login page (`/login`).
- Enter an incorrect username or password.
- This will log an authentication failure event.

### 3. Unauthorized Access Attempt

- Without logging in, try to access the create credit card page (`/create_credit_card`) or view a credit card (`/view_credit_card/1`).
- This will log an unauthorized access attempt.

### 4. Credit Card Creation and Viewing

- Log in with a valid account.
- Create a new credit card (this action is logged).
- View the created credit card (this access is also logged).

## Security Logging Implementation

The security logging in this app is implemented using Python's built-in `logging` module. Here's how it works:

1. **Log Configuration**: In `app.py`, we configure logging using `dictConfig`. This sets up a file handler that writes log messages to `security.log`.

2. **Log Levels**: We use different log levels for various events:
   - `WARNING` for security violations (e.g., failed logins, unauthorized access attempts)
   - `INFO` for normal operations (e.g., successful logins, credit card creations)

3. **Logging in Code**: Throughout the application, we use `app.logger` to log events. For example:
   ```python
   app.logger.warning(f"Failed login attempt for username: {username}")
   app.logger.info(f"Credit card created for user_id: {session['user_id']}")
   ```

4. **Structured Logging**: The log messages include timestamps, log levels, and contextual information, making it easy to analyze security events.

## Security Considerations

- Passwords are hashed using Werkzeug's `generate_password_hash` function.
- User sessions are managed securely using Flask's session management.
- Input validation is performed on the server-side to prevent malformed data.
- Sensitive operations (like viewing credit cards) check for user authentication and authorization.

## Future Improvements

- Implement HTTPS for secure communication.
- Add rate limiting to prevent brute-force attacks.
- Implement multi-factor authentication for enhanced security.
- Use a more robust database system for production environments.

## Conclusion

This Secure Flask App demonstrates basic principles of security logging and secure web application development. It serves as a starting point for building more comprehensive secure web applications with proper logging and monitoring capabilities.