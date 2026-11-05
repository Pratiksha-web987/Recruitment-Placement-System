import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

# Load .env from project root folder
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "rpms_db")
        )

        return connection

    except mysql.connector.Error as error:
        print("Database Connection Failed:", error)
        return None


if __name__ == "__main__":
    db = create_connection()

    if db:
        print("RPMS Database Connected Successfully!")
        db.close()
        print("Database Connection Closed.")