## Project Structure

- **migrations/**: Contains database migration scripts.
- **src/**: Contains the main source code of the project.
- **.gitignore**: Specifies files and directories ignored by Git.
- **alembic.ini**: Configuration file for Alembic, a database migration tool for SQLAlchemy.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Setup Instructions

Follow these steps to set up and run the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OLoghunov/study-scope.git
   cd study-scope
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
   Ensure that your database settings are correctly configured in the `alembic.ini` file.

5. **Apply database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Run the application**:
   ```bash
   fastapi dev src
   ```

## Additional Notes

- The project uses Alembic for database migrations. Ensure you have the correct database connection string configured in `alembic.ini`.
- Refer to the `requirements.txt` file for the list of dependencies and their versions.
- Make sure that your Redis server is working correctly.

## Contributing

Feel free to fork this repository, submit issues, or create pull requests to improve the project.

## License

This project is licensed under the MIT License.

---

If you encounter any issues or have questions, please open an issue in this repository.
