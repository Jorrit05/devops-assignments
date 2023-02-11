import os
import pymongo

from swagger_server.models.student import Student  # noqa: E501
from bson.json_util import dumps, ObjectId

import logging


log = logging.getLogger("student_service")

# Connect to the MongoDB database running in the container
connection_string = os.getenv("MONGO_URI")
client = pymongo.MongoClient(connection_string)

# Get the database (the database will be created automatically if it doesn't exist)
db = client["student_db"]

# Get the collection (the collection will be created automatically if it doesn't exist)
collection = db["student_collection"]


def add(student=None):
    log.warning(f"type: {type(student)}")

    # Find student by first, last name combination
    result = collection.find_one({"first_name": student["first_name"], "last_name": student["last_name"]})
    if result:
        return 'user already exists', 409

    # return student ID, field: _ID
    return str(collection.insert_one(student).inserted_id)

def get_by_id(student_id=None, subject=None):

    try:
        student = collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            return 'not found', 404
    except:
        # Invalid ID formats simply return not found
        log.warning("Invalid ID")
        return 'not found', 404


    return dumps(student)

def delete(student_id=None):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    result = collection.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count > 0:
        return f"deleted {student_id}"

    return "Something went wrong", 500
