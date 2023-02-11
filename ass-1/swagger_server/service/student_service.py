import os
import tempfile
from functools import reduce
import pymongo

from swagger_server.models.student import Student  # noqa: E501
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS, loads, ObjectId

import json
import logging
import bson

log = logging.getLogger("student_service")
from tinydb import TinyDB, Query

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

# Connect to the MongoDB database running in the container
client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")

# Get the database (the database will be created automatically if it doesn't exist)
db = client["student_db"]

# Get the collection (the collection will be created automatically if it doesn't exist)
collection = db["student_collection"]


def add(student=None):
    log.warning(f"type: {type(student)}")

    result = collection.find_one({"first_name": student["first_name"], "last_name": student["last_name"]})
    if result:
        return 'user already exists', 409

    return str(collection.insert_one(student).inserted_id)

    # try:
    #     log.info(student["student_id"])
    # except KeyError:
    #     # No student ID was given, insert the field an return the ID
    #     log.warning("No Key given ")
    #     student["student_id"] = collection.insert_one(student).inserted_id
    #     collection.update_one({"_id": student["student_id"]}, {"$set": {"student_id": student["student_id"]}})
    #     return str(student["student_id"])
    # ID +=1
    # student["_id"] = ID
    # log.info(f"Inserting {student}")
    # collection.insert_one(student).inserted_id

    # return str(student["student_id"])
    # print(student)
    # log.warning(db_file_path)
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
    # return student.student_id


def get_by_id(student_id=None, subject=None):

    try:
        student = collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            return 'not found', 404
    except:
        log.warning("Invalid ID")
        return 'not found', 404


    return dumps(student)
    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return 'not found', 404
    # student['student_id'] = student_id
    # print(student)
    # return student

def delete(student_id=None):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    result = collection.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count > 0:
        return f"deleted {student_id}"

    return "Something went wrong", 500

    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return 'not found', 404
    # student_db.remove(doc_ids=[int(student_id)])
    # return student_id



    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return 'not found', 404
    # student_db.remove(doc_ids=[int(student_id)])
    # return student_id