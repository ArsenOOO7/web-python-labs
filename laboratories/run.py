from os import environ as env

from app import app

if __name__ == "__main__":
    app.run(port=env.get("PORT") or 5000)
