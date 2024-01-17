# import json
# import jsonschema
# import sys
# import requests
# import uuid
# import os
#
#
# def is_json_file(file_path):
#     _, file_extension = os.path.splitext(file_path)
#     return file_extension.lower() == '.json'
#
# def process_files(filename):
#     try:
#         with open(filename, 'r') as file:
#             data_graph = file.read()
#     except FileNotFoundError:
#         print(f"Error: File '{filename}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     schema = {
#         "type": "object",
#         "properties" : {
#             "MineralSite": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties" : {
#                         "id" : {"type" : "number"},
#                         "name" : {"type" : "string"},
#                         "source_id" : {"type" : "string"},
#                         "record_id" : {"type" : "number"},
#                         "location_info": {
#                             "type": "object",
#                             "properties": {
#                                 "location": {"type": "string"},
#                                 "country": {"type": "string"},
#                                 "state_or_province": {"type": "string"},
#                                 "location_source_record_id": {"type": "string"},
#                                 "crs": {"type": "string"},
#                                 "location_source": {"type": "string"}
#                             }
#                         },
#                         "deposit_type" : {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "properties": {
#                                     "id": {"type": "string"}
#                                 }
#                             }
#                         },
#                         "geology_info": {
#                             "type": "object",
#                             "properties": {
#                                 "age": {"type": "string"},
#                                 "unit_name": {"type": "string"},
#                                 "description": {"type": "string"},
#                                 "lithology": {"type": "string"},
#                                 "process": {"type": "string"},
#                                 "comments": {"type": "string"},
#                                 "environment": {"type": "string"}
#                             }
#                         },
#                         "MineralInventory": {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "properties": {
#                                     "id": {"type": "number"},
#                                     "category": {"type": "string"},
#                                     "contained_metal": {"type": "number"},
#                                     "reference": {
#                                         "type": "object",
#                                         "properties": {
#                                             "id": {"type": "number"},
#                                             "document": {
#                                                 "type": "object",
#                                                 "properties": {
#                                                     "id": {"type": "string"},
#                                                     "title": {"type": "string"},
#                                                     "doi": {"type": "string"},
#                                                     "uri": {"type": "string"},
#                                                     "journal": {"type": "string"},
#                                                     "year": {"type": "number"},
#                                                     "month": {"type": "number"},
#                                                     "volume": {"type": "number"},
#                                                     "issue": {"type": "number"},
#                                                     "description": {"type": "string"},
#                                                     "authors": {
#                                                         "type": "array",
#                                                         "items": {"type": "string"}
#                                                     }
#                                                 }
#                                             },
#                                             "page_info": {
#                                                 "type": "array",
#                                                 "items": {
#                                                     "type": "object",
#                                                     "properties": {
#                                                         "page": {"type": "number"},
#                                                         "bounding_box": {
#                                                             "type": "object",
#                                                             "properties": {
#                                                                 "x_min": {"type": ["string", "number"]},
#                                                                 "x_max": {"type": ["string", "number"]},
#                                                                 "y_min": {"type": ["string", "number"]},
#                                                                 "y_max": {"type": ["string", "number"]}
#                                                             },
#                                                             "required": ["x_min", "x_max", "y_min", "y_max"]
#                                                         }
#                                                     },
#                                                     "required": ["page"]
#                                                 }
#
#                                             }
#                                         }
#                                     },
#                                     "date": {"type": "string", "format": "date"},
#                                     "commodity": {"type": "string"},
#                                     "ore": {
#                                         "type": "object",
#                                         "properties": {
#                                             "ore_unit": {"type": "string"},
#                                             "ore_value": {"type": "number"}
#                                         }
#                                     },
#                                     "grade": {
#                                         "type": "object",
#                                         "properties": {
#                                             "grade_unit": {"type": "string"},
#                                             "grade_value": {"type": "number"}
#                                         }
#
#                                     },
#                                     "cutoff_grade": {
#                                         "type": "object",
#                                         "properties": {
#                                             "grade_unit": {"type": "string"},
#                                             "grade_value": {"type": "number"}
#                                         }
#                                     }
#                                 },
#                                 "required": ["reference"]
#
#                             }
#                         }
#                     },
#                     "required": ["name"]
#                 },
#                 "required": ["source_id", "record_id"]
#             }
#         }
#     }
#
#     with open(filename) as file:
#         json_data = json.load(file)
#     json_string = json.dumps(json_data)
#     mineral_site_json = json.loads(json_string)
#
#     try:
#         jsonschema.validate(instance=mineral_site_json, schema=schema)
#         print("Validation succeeded")
#     except jsonschema.ValidationError as e:
#         print(f"Validation failed: {e}")
#         raise  # Raise an exception to indicate failure
#
#
# changed_files = sys.argv[1:]
#
# for file_path in changed_files:
#     if is_json_file(file_path):
#         print(f'{file_path} is a JSON file')
#         process_files(file_path)
#     else:
#         print(f'{file_path} is not a JSON file')
#
#
# # print(type(json_data))

import sys

try:
    # Your script logic here
    result = 1 / 0  # Some error
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)  # Exit with status code 1 for failure
