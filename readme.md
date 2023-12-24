# Community Event Planner

## Introduction
The Community Event Planner is a comprehensive backend API designed to facilitate event management, user interaction, and community engagement. It serves as a robust platform for users to create, browse, and interact with events through comments, providing a streamlined process for organizing and participating in community events.

## Technologies and Frameworks

### FastAPI
**Usage**: FastAPI is the core web framework for our API. It's a modern, fast (high-performance) framework for building APIs with Python 3.7+ based on standard Python type hints. In this project, FastAPI handles all the routing, requests, and responses.

### PostgreSQL
**Usage**: PostgreSQL is our chosen database for this project due to its robustness, performance, and compatibility with complex operations and queries. It stores all user, event, and comment data, ensuring data integrity and providing advanced query capabilities.

### SQLAlchemy
**Usage**: SQLAlchemy is the SQL toolkit and ORM we've implemented for database interactions. It provides a full suite of well-known enterprise-level persistence patterns and is designed for efficient and high-performing database access.

### Pydantic
**Usage**: Pydantic is used for data validation and settings management using Python type annotations. Pydantic ensures that incoming data is of the correct type and meets all defined criteria before the application processes it, providing an additional layer of security and reliability.

### python-jose and Passlib
**Usage**: python-jose is utilized to handle JWT tokens for secure and efficient user authentication. Passlib is a password hashing library used to securely store and verify user passwords.

### Alembic
**Usage**: Alembic, a lightweight database migration tool, is used to handle schema changes. It allows us to modify the database schema without losing data or compromising the existing setup.

## Features
- **User Authentication**: Securely register and authenticate users, managing sessions through JWT tokens.
- **Event Management**: Users can create, update, browse, and delete events, with details like title, description, date, and location.
- **Comments**: Users can post comments on events, facilitating community discussion and interaction.
- **Data Validation**: Extensive use of Pydantic models ensures that all data received and sent via the API meets our stringent requirements.
- **Security**: Passwords are securely hashed using Bcrypt, and sensitive routes are protected with JWT-based authentication.

## Project Structure

- `app/models`: Contains SQLAlchemy models for User, Event, and Comment.
- `app/routes`: FastAPI routers handling the API endpoints for different entities.
- `app/schemas`: Pydantic models for request and response data validation.
- `app/services`: Business logic for user authentication, CRUD operations, and database connection.

## Getting Started

1. **Set up Python environment**: Ensure Python 3.7+ is installed.
2. **Install dependencies**: Run `pip install -r requirements.txt`.
3. **Set up PostgreSQL**: Ensure a PostgreSQL instance is running and accessible.
4. **Configure Environment Variables**: Set `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` in your `.env` file.
5. **Run the application**: Execute `uvicorn main:app --reload` to start the FastAPI server.
6. **Test the endpoints**: Use the auto-generated Swagger UI at `/docs` for easy testing and interaction.

## Testing

- **Unit Tests**: Test individual components using Pytest. Run tests with `pytest`.
- **Integration Tests**: Test the API routes and their interaction with the database.

## Deployment

The application is container-ready with a Dockerfile. For production deployment, consider using a Docker orchestration system like Docker Swarm or Kubernetes.

## Contribution

Contributions are welcome! Please fork the repository and open a pull request with your proposed changes. Ensure that your code adheres to the project's style and has sufficient test coverage.
