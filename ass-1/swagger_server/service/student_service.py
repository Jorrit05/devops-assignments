import os
import tempfile
from functools import reduce
import pymongo

from swagger_server.models.student import Student  # noqa: E501
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS, loads

import json
import logging
import bson

log = logging.getLogger("student_service")
# from tinydb import TinyDB, Query

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

# Connect to the MongoDB database running in the container
client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")

# Get the database (the database will be created automatically if it doesn't exist)
db = client["student_db"]

# Get the collection (the collection will be created automatically if it doesn't exist)
collection = db["student_collection"]


def add(student=None):
    result = collection.find_one({"student_id": student["student_id"]})
    if result:
        return 'user already exists', 409

    log.info(f"Inserting {student}")

    return f"Inserted id {collection.insert_one(student).inserted_id}"
    # if collection.find({"student_id": student["student_id"]}):
    #     return 'user already exists', 409

    # log.info(f"Inserting {student}")
    # return collection.insert_one(student)
    # Confirm that the document has been added


    # queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)
    # res = student_db.search(query)
    # if res:
    #     return 'already exists', 409

    # doc_id = student_db.insert(student.to_dict())
    # student.student_id = doc_id
    return student["student_id"]


def get_by_id(student_id=None, subject=None):
    student = collection.find_one({"student_id": student_id})
    # student = student_db.get(doc_id=int(student_id))

    if not student:
        return 'not found', 404

    return dumps(student)


def delete(student_id=None):
    student = collection.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404

    result = collection.delete_one({"student_id": student_id})

    if result.deleted_count > 0:
        return f"deleted {student_id}"

    return "Something went wrong", 500




    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return 'not found', 404
    # student_db.remove(doc_ids=[int(student_id)])
    # return student_id