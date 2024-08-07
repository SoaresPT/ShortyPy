
## Getting Started

### Prerequisites

- Python 3.9+
- Virtual Environment (recommended)

### Setup

Follow these steps to set up the project on your local machine.

1. **Clone the Repository**

   ```sh
   git clone https://github.com/SoaresPT/ShortyPy.git
   cd ShortyPy
   ```

2. **Create and Activate a Virtual Environment**

   - On macOS/Linux:

     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:

     ```sh
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install the Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file by copying the `.env.example` file and filling in your settings.

   ```sh
   cp .env.example .env
   ```

   Fill in your `.env` file with the appropriate values:

   ```env
   JWT_SECRET=my_secret_key
   DATABASE_URL=sqlite:///my_database.db
   API_ENDPOINT=/shortypy
   ```

5. **Run Database Migrations**

   Use Alembic to run the initial database migration:

   ```sh
   alembic upgrade head
   ```

### Running the Application

Start the FastAPI application using Uvicorn:

```sh
python -m uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser to see the application running.
