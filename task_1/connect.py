import configparser
import pathlib

from mongoengine import connect

file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

try:
    connect(
        host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority",
        ssl=True,
    )
except Exception as error:
    print(f"Failed to connect to MongoDB: {error}")
