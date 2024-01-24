import json
import jsonschema
import sys
import requests
import uuid
import os
import generate_uris

def mineral_site_uri(data):
    response = generate_uris.mineral_site_uri(data)
    uri = ''
    print(response)
    uri = response['result']
    return uri

def document_uri(data):
    response = generate_uris.document_uri(data)
    uri = ''
    uri = response['result']
    return uri

def mineral_inventory_uri(param1):
    response = generate_uris.mineral_inventory_uri(param1)
    uri = ''
    uri = response['result']
    return uri


def is_json_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.json'


def update_pull_request(file_content, file_path):
    pull_request_number = os.environ.get('GITHUB_REF').split('/')[-2]
    github_token = os.environ.get('GITHUB_TOKEN')
    print(github_token)
    print(os.environ.get('GITHUB_REF'))

    url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/pulls/{pull_request_number}/files/{file_path}'

    url2 = "https://api.github.com/repos/:owner/:repo/pulls/:number"

    print(url)
    headers = {'Authorization': f'token {github_token}'}

    response = requests.put(url, headers=headers, json={'content': file_content})

    if response.status_code == 200:
        print(f'Successfully updated file in pull request #{pull_request_number}')
    else:
        print(f'Failed to update file. Status code: {response.status_code}, Response: {response.text}')

def process_files(filename):
    try:
        with open(filename, 'r') as file:
            data_graph = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    schema = {
        "type": "object",
        "properties" : {
            "MineralSite": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties" : {
                        "id" : {"type" : "string"},
                        "name" : {"type" : "string"},
                        "source_id" : {"type" : "string"},
                        "record_id" : {"type" : "number"},
                        "location_info": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string"},
                                "country": {"type": "string"},
                                "state_or_province": {"type": "string"},
                                "location_source_record_id": {"type": "string"},
                                "crs": {"type": "string"},
                                "location_source": {"type": "string"}
                            }
                        },
                        "deposit_type" : {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"}
                                }
                            }
                        },
                        "geology_info": {
                            "type": "object",
                            "properties": {
                                "age": {"type": "string"},
                                "unit_name": {"type": "string"},
                                "description": {"type": "string"},
                                "lithology": {"type": "string"},
                                "process": {"type": "string"},
                                "comments": {"type": "string"},
                                "environment": {"type": "string"}
                            }
                        },
                        "MineralInventory": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "category": {"type": "string"},
                                    "contained_metal": {"type": "number"},
                                    "reference": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "number"},
                                            "document": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "doi": {"type": "string"},
                                                    "uri": {"type": "string"},
                                                    "journal": {"type": "string"},
                                                    "year": {"type": "number"},
                                                    "month": {"type": "number"},
                                                    "volume": {"type": "number"},
                                                    "issue": {"type": "number"},
                                                    "description": {"type": "string"},
                                                    "authors": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    }
                                                }
                                            },
                                            "page_info": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "page": {"type": "number"},
                                                        "bounding_box": {
                                                            "type": "object",
                                                            "properties": {
                                                                "x_min": {"type": ["string", "number"]},
                                                                "x_max": {"type": ["string", "number"]},
                                                                "y_min": {"type": ["string", "number"]},
                                                                "y_max": {"type": ["string", "number"]}
                                                            },
                                                            "required": ["x_min", "x_max", "y_min", "y_max"]
                                                        }
                                                    },
                                                    "required": ["page"]
                                                }

                                            }
                                        }
                                    },
                                    "date": {"type": "string", "format": "date"},
                                    "commodity": {"type": "string"},
                                    "ore": {
                                        "type": "object",
                                        "properties": {
                                            "ore_unit": {"type": "string"},
                                            "ore_value": {"type": "number"}
                                        }
                                    },
                                    "grade": {
                                        "type": "object",
                                        "properties": {
                                            "grade_unit": {"type": "string"},
                                            "grade_value": {"type": "number"}
                                        }

                                    },
                                    "cutoff_grade": {
                                        "type": "object",
                                        "properties": {
                                            "grade_unit": {"type": "string"},
                                            "grade_value": {"type": "number"}
                                        }
                                    }
                                },
                                "required": ["reference"]

                            }
                        }
                    },
                    "required": ["name"]
                },
                "required": ["source_id", "record_id"]
            }
        }
    }

    with open(filename) as file:
        json_data = json.load(file)
    json_string = json.dumps(json_data)
    mineral_site_json = json.loads(json_string)

    try:
        jsonschema.validate(instance=mineral_site_json, schema=schema)
        print("Validation succeeded")
    except jsonschema.ValidationError as e:
        print(f"Validation failed: {e}")
        raise  # Raise an exception to indicate failure


changed_files = sys.argv[1:]

print('Running this')
print(changed_files)

for file_path in changed_files:
    if is_json_file(file_path):
        print(f'{file_path} is a JSON file')
        process_files(file_path)
        json_data=''
        with open(file_path) as file:
            json_data = json.load(file)

        json_string = json.dumps(json_data)
        mineral_site_json = json.loads(json_string)

        ms_list = json_data['MineralSite']
        mndr_url = 'https://minmod.isi.edu/resource/'

        for ms in ms_list:
            mi_data = {
                "site": ms
            }

            ms['id'] = mndr_url + mineral_site_uri(mi_data)
            if "MineralInventory" in ms:

                mi_list = ms['MineralInventory']

                counter = 0

                for mi in mi_list:
                    mi_data = {
                        "site": ms,
                        "id": counter
                    }
                    mi['id'] = mndr_url + mineral_inventory_uri(mi_data)
                    counter += 1

                    if "reference" in mi:
                        reference = mi['reference']
                        if "document" in reference:
                            document = reference['document']

                            doc_data = {
                                "document": document
                            }

                            document['id'] = mndr_url + document_uri(doc_data)


        update_pull_request(json.dumps(json_data, indent=2), file_path)





    else:
        print(f'{file_path} is not a JSON file')


# print(type(json_data))