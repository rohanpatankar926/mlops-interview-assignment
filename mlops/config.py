import pymongo
import os
from dataclasses import dataclass


TARGET_COLUMN="label"

@dataclass
class EnvironmentVariable(object):
    mongodb_url:str="mongodb+srv://rohanpatankar926:1234@main.ncl3zpm.mongodb.net/"

env_var=EnvironmentVariable()
mongo_client=pymongo.MongoClient(env_var.mongodb_url)