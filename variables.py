import os
import sys
import pymongo
import json
import ssl

# Check if the environment variables are set
if 'MONGO_URL' not in os.environ:
    print("Please set the MONGO_URL environment variable.")
    sys.exit(1)

# Retrieve the values of environment variables
connection_string = os.environ['MONGO_URL']

db_name = "ssm"  # Replace 'your_database' with your database name
collection_name = "variables"  # Replace 'ss' with your collection name
file_name = '.env'  # Specify the file name

class ProjectNotFoundError(Exception):
    pass

# Accepting project_name as an argument
if len(sys.argv) < 2:
    print("Usage: python script.py project_name")
    sys.exit(1)

project_name = sys.argv[1]

client = pymongo.MongoClient(
    connection_string,
    tls=True,
    tlsAllowInvalidCertificates=False,
    tlsVersion=ssl.PROTOCOL_TLSv1_2
)
# client = pymongo.MongoClient(connection_string)

# Accessing the database
db = client[db_name]

# Accessing the collection
collection = db[collection_name]

# Find the record where the project name is provided as an argument
result = collection.find_one({"project": project_name})

# Extracting and storing the 'vars' attribute or raising an error if the project does not exist
if result and 'vars' in result:
    vars_data = result['vars']
    with open(file_name, 'w') as file:
        for key, value in vars_data.items():
            file.write(f"{key}={value}\n")
else:
    raise ProjectNotFoundError(f"Project '{project}' does not exist in the database.")
