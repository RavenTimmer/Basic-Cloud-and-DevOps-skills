import os
from pymongo import MongoClient
from bson import ObjectId

mongo_uri = os.environ.get('MONGO_URI', 'mongodb://mongo:27017')
client = MongoClient(mongo_uri)
db = client['students_db']
students_collection = db['students']


def add(student=None):
    student.student_id = None

    existing = students_collection.find_one({
        'first_name': student.first_name,
        'last_name': student.last_name
    })
    if existing:
        return 'already exists', 409

    doc_id = students_collection.insert_one(student.to_dict()).inserted_id
    student.student_id = str(doc_id)
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404
    student['student_id'] = str(student['_id'])
    # MongoDB is weird and gives a id that cant be parsed. Since this is a test project this fix.
    student.pop('_id', None)
    return student


def delete(student_id=None):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404
    students_collection.delete_one({"_id": ObjectId(student_id)})
    return student_id


def get_average_grade(student_id=None):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    grade_records = student.get('grade_records', [])
    if not grade_records or len(grade_records) == 0:
        return 'no grades found', 404

    total_grade = sum(record.get('grade', 0) for record in grade_records)
    average_grade = total_grade / len(grade_records)
    return average_grade