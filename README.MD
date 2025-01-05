# Steps to Populate the Database, Create a Super User, and Run the Application

## Step 1: Prepare and Populate the Database

1. Open your terminal and navigate to the project directory.
2. Activate the virtual environment:

    ```sh
    source .venv/bin/activate
    ```

3. Run the following command to clean the CSV files:

    ```sh
    python clean_csv.py
    ```

4. Run the following command to create the migration files:

    ```sh
    python manage.py makemigrations
    ```

5. Run the following command to apply the migrations:

    ```sh
    python manage.py migrate
    ```

6. Run the following command to populate the database with data from CSV files:

    ```sh
    python scripts/populate_data.py
    ```

## Step 2: Create a Super User

1. In the terminal, run the following command to create a super user:

    ```sh
    python manage.py createsuperuser
    ```

2. When prompted, enter the following details:
    - Username: [admin](http://_vscodecontentref_/0)
    - Email: [admin@admin.com](http://_vscodecontentref_/1)
    - Password: [admin](http://_vscodecontentref_/2)

## Step 3: Run the Application

1. In the terminal, run the following command to start the Django development server:

    ```sh
    python manage.py runserver
    ```

2. Open your web browser and navigate to [http://127.0.0.1:8000/admin](http://_vscodecontentref_/3).
3. Log in with the super user credentials you created:
    - Username: [admin](http://_vscodecontentref_/4)
    - Password: [admin](http://_vscodecontentref_/5)

You should now be able to access the Django admin site and manage your application.

## Step 4: View API Documentation

1. To view the Swagger UI for your API documentation, navigate to:

    ```sh
    http://127.0.0.1:8000/swagger/
    ```

2. To view the ReDoc UI for your API documentation, navigate to:

    ```sh
    http://127.0.0.1:8000/redoc/
    ```

3. To view the raw JSON schema of your API, navigate to:

    ```sh
    http://127.0.0.1:8000/swagger.json
    ```

## Step 5: Test the Application

1. To run all tests, use the following command:

    ```sh
    python manage.py test
    ```

2. To run tests from a specific test module, use the following command:

    ```sh
    # test api
    python manage.py test mortometricsapp.tests_api

    # test serializer
    python manage.py test mortometricsapp.tests_serializer
    ```
