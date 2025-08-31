from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # print("db :", os.getenv("SUPABASE_DB_URI"))
    # with app.app_context():
    #     print("Available routes:")
    #     for rule in app.url_map.iter_rules():
    #         print(rule)

    app.run(host='0.0.0.0', debug=True, port=5000)
