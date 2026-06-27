import os


class Settings:
    # Central config object for app-wide settings like secrets and URLs.
    secret_key = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")


settings = Settings()
