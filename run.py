from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    print("db :", os.getenv("SUPABASE_DB_URI"))

    app.run(debug=True, port=5000)