"""Reads all settings from environment variables (loaded from the .env file)."""
import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file in the project folder


def _require(name):
    """Return an environment variable or stop with a clear message."""
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "Copy .env.example to .env and fill in your values."
        )
    return value


class Config:
    SECRET_KEY = _require("SECRET_KEY")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = _require("DB_USER")
    DB_PASSWORD = _require("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "attendease")