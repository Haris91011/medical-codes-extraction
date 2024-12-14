# # app/core/config.py

# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv
# import os

# load_dotenv()





# class Settings(BaseSettings):
#     """
#     This Settings class is designed to load and manage environment variables for an
#     application using Pydantic's BaseSettings and python-dotenv

#     write all your env variables here so you can access them easily.

#     """


#     MSSQL_SERVER:str = os.environ.get("MSSQL_SERVER")
#     MSSQL_DATABASE:str = os.environ.get("MSSQL_DATABASE")
#     MSSQL_USER : str = os.environ.get("MSSQL_USER")
#     MSSQL_PASSWORD : str = os.environ.get("MSSQL_PASSWORD")
#     OPENAI_API_KEY : str = os.environ.get("OPENAI_API_KEY")
#     DB_HOST : str = os.environ.get("DB_HOST")
#     DB_USER : str = os.environ.get("DB_USER")
#     DB_PASSWORD : str = os.environ.get("DB_PASSWORD")
#     DB_NAME : str = os.environ.get("DB_NAME")


#     class Config:
#         env_file = ".env"

# settings = Settings()

# app/core/config.py

import toml
from pydantic import BaseModel

class Settings(BaseModel):
    """
    This Settings class is designed to load and manage configuration variables
    from a secrets.toml file using Pydantic's BaseModel.
    """

    # Load secrets from the secrets.toml file
    secrets = toml.load("secrets.toml")

    # Define your environment variables
    MSSQL_SERVER: str = secrets["database"]["mssql_server"]
    MSSQL_DATABASE: str = secrets["database"]["mssql_database"]
    MSSQL_USER: str = secrets["database"]["mssql_user"]
    MSSQL_PASSWORD: str = secrets["database"]["mssql_password"]
    OPENAI_API_KEY: str = secrets["api"]["openai_api_key"]
    DB_HOST: str = secrets["database"]["db_host"]
    DB_USER: str = secrets["database"]["db_user"]
    DB_PASSWORD: str = secrets["database"]["db_password"]
    DB_NAME: str = secrets["database"]["db_name"]


# Create an instance of the settings
settings = Settings()
