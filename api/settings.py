# System Imports
import os
from functools import lru_cache

# Package Imports
from dotenv import dotenv_values


@lru_cache
def get_settings():
    return Settings()


# load .env values
env = {
    **os.environ,  # load system environment variables
    **dotenv_values(),  # load .env file
}


class Settings:
    OPENAI_API_KEY: str = env.get("OPENAI_API_KEY")
