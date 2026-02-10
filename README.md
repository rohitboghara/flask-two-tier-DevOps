# Flask Two-Tier Application

This is a Flask-based web application demonstrating a two-tier architecture, separating the presentation layer from the data layer. It includes user management functionalities (CRUD operations) and is set up with Docker, Docker Compose, Kubernetes configurations, and integrated with monitoring tools like Prometheus and Grafana, and CI/CD with Jenkins.

## Features

-   **User Management:** Add, view, update, and delete users.
-   **Two-Tier Architecture:** Clear separation between the Flask presentation layer and a PostgreSQL data layer.
-   **Containerization:** Dockerfile for the Flask application and Docker Compose for local development setup of the application and PostgreSQL.
-   **Orchestration:** Kubernetes deployment configurations for Flask and PostgreSQL.
-   **Monitoring:** Integrated with Prometheus for metrics collection and Grafana for visualization.
-   **CI/CD:** Jenkinsfile for continuous integration and continuous deployment.
-   **CSRF Protection:** Implemented using Flask-WTF.

## Technologies Used

-   **Backend:** Flask (Python)
-   **Database:** PostgreSQL
-   **Containerization:** Docker, Docker Compose
-   **Orchestration:** Kubernetes
-   **Monitoring:** Prometheus, Grafana, `prometheus-flask-exporter`, `psutil`
-   **CI/CD:** Jenkins
-   **Forms & CSRF:** Flask-WTF
-   **Database Driver:** `psycopg2-binary`
-   **WSGI Server:** Gunicorn

## Setup and Installation

### Prerequisites

-   Docker
-   Docker Compose
-   kubectl (for Kubernetes deployments)

### Local Development with Docker Compose

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd flask-two-tier
    ```

2.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` and fill in the necessary environment variables, especially for the database connection.

    ```bash
    cp .env.example .env
    ```

    Example `.env` content:
    ```
    SECRET_KEY=your_secret_key_here
    DATABASE_HOST=db
    DATABASE_NAME=userdb
    DATABASE_USER=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_PORT=5432
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=8000
    FLASK_ENV=development
    ```

3.  **Build and run the services:**
    ```bash
    docker-compose up --build -d
    ```

    This will start the Flask application and the PostgreSQL database.

4.  **Access the application:**
    The Flask application will be available at `http://localhost:8000` (or the port specified in your `.env` file).

5.  **Access Monitoring Tools:**
    -   **Prometheus:** `http://localhost:9090`
    -   **Grafana:** `http://localhost:3000` (default credentials: `admin`/`admin`)

### Running with Kubernetes

(Instructions for deploying to Kubernetes would go here, referencing the files in the `kubernetes/` directory)

### Running Locally (without Docker)

1.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Same as step 2 in local development. Ensure `DATABASE_HOST` points to your local PostgreSQL instance or `localhost` if running PostgreSQL directly.

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

    The application will run on `http://127.0.0.1:8000` by default.

## Project Structure

```
.
├───.env.example
├───app.py
├───config.py
├───data_layer.py
├───docker-compose.yml
├───Dockerfile
├───Jenkinsfile
├───README.md
├───requirements.txt
├───grafana/
├───jenkins/
├───kubernetes/
│   ├───flask-web-deployment.yml
│   ├───namespace.yml
│   ├───postgres-deployment.yml
│   └───config/
├───prometheus/
├───routes/
│   ├───__init__.py
│   ├───health_routes.py
│   └───main_routes.py
├───sonrqube/
├───templates/
│   ├───add_user.html
│   ├───base.html
│   ├───index.html
│   └───update_user.html
└───venv/
```

## Contributing

(Instructions for contributing would go here)

## License

(License information would go here)
