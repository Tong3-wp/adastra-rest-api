# FastAPI API Project

Submission for Adastra – REST API assessment

## Instruction

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Tong3-wp/adastra-rest-api.git
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables:**

    * Create a `.env` file in the root directory.
    * Add DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES.
    * Example at `.env.example`

5.  **Run the Database:**

    ```bash
    docker compose up db -d
    ```

6.  **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    Visit http://localhost:8000/docs to view the API docs

7.  **Run tests:**

    ```bash
    pytest --cov=app tests/
    ```

## Generate image and run on container with Docker

1.  **Build the Docker image and run the Docker container:**

    ```bash
    docker compose up --build -d 
    ```

    Visit http://127.0.0.1:8000/docs to view the API docs
