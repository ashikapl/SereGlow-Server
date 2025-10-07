from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # for local dev you can enable debug from env, but don't hardcode debug=True
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
