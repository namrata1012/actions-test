import json
import jsonschema
import sys
import requests
import uuid
import os
import generate_uris
import base64
import subprocess

from drepr.engine import execute, DRepr, FileOutput, OutputFormat

def get_sha(owner, repo, path, branch):
    # repository = os.environ["GITHUB_REPOSITORY"]
    #
    # url = f'https://api.github.com/repos/{repository}/contents/{file_path}'
    #
    # headers = {
    #     'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}',
    #     'Accept': 'application/vnd.github.v3+json',
    # }
    #
    # response = requests.get(url, headers=headers)

    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        content = response.json()
        return content['sha']
    else:
        print(f"Error: {response.status_code}")
        return None

    sha = None

# Check if the request was successful
    if response.status_code == 200:
    # File exists, update it
        sha = response.json()['sha']
        return sha
    else:
    # File doesn't exist, create it
        sha = None
    return sha


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
    path, file_extension = os.path.splitext(file_path)
    print(str(path))
    split_path = path.split('/')
    is_under_data_folder = False
    if len(split_path) == 2 and split_path[0] == 'inferlink':
        print('This is under data folder')
        is_under_data_folder = True

    return is_under_data_folder and file_extension.lower() == '.json'


def file_datasource(file_path):
    path, file_extension = os.path.splitext(file_path)
    split_path = path.split('/')
    if len(split_path) == 2 and split_path[0] == 'inferlink':
        print('This is under data folder')
        return split_path[0]
    return ''


def run_drepr_on_file(datasource):
    destination = 'generated_files/ttl_files/'
    model_file = 'model.yml'
    command = f' python -m drepr -r {model_file} -d default="generated_files/json_files/MVT_Zinc.json"'
    print('Running ... ', command)

    # Run the command
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output_lines = result.stdout.splitlines()[2:]  # Skip the first two lines
        return '\n'.join(output_lines)

        # Replace 'output_file.txt' with the desired file name
        #     with open('output_file.txt', 'w') as file:
        #         file.write('\n'.join(output_lines))
        print("Command output (skipping first two lines) written to 'output_file.txt'")
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        print("Command output (if any):", e.output)
        return ''

def create_drepr_update_github(file_path, filename):
    pull_request_number = os.environ.get('GITHUB_REF').split('/')[-2]
    github_token = os.environ.get('GITHUB_TOKEN')
    print(github_token)
    print(os.environ.get('GITHUB_REF'))

    generated_ttl_path = f'generated_files/ttl_files/{filename}.ttl'
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json',
    }
    # owner, repo, path, branch
    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ["GITHUB_HEAD_REF"]
    url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/contents/{generated_ttl_path}'
    print(url)
    existing_sha = get_sha('namrata1012', repo, file_path, branch)
    file_content = run_drepr_on_file(file_path)
    encoded_content = base64.b64encode(file_content.encode()).decode()
    payload = {
        'message': 'Update file via GitHub Actions',
        'content': encoded_content,
        'branch': branch,
        'sha':existing_sha
    }

    # Make the API request to update the file
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f'Successfully updated file in pull request #{pull_request_number}')
    else:
        print(f'Failed to update file. Status code: {response.status_code}, Response: {response.text}')

    return

def update_pull_request(file_content, file_path):
    pull_request_number = os.environ.get('GITHUB_REF').split('/')[-2]
    github_token = os.environ.get('GITHUB_TOKEN')
    print(github_token)
    print(os.environ.get('GITHUB_REF'))

    url = f'https://api.github.com/repos/namrata1012/{os.environ["GITHUB_REPOSITORY"]}/pulls/{pull_request_number}/files/{file_path}'

    url2 = "https://api.github.com/repos/:owner/:repo/pulls/:number"

# curl -L \
# -X PUT \
#    -H "Accept: application/vnd.github+json" \
#       -H "Authorization: Bearer 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" \
#          -H "X-GitHub-Api-Version: 2022-11-28" \
#     https://api.github.com/repos/namrata1012/actions-test/contents/abc.json \
#             -d '{"message":"my commit message”, “branch”:”test-pr" ,”committer":{"name":"Monalisa Octocat","email":"octocat@github.com"},"content":"bXkgbmV3IGZpbGUgY29udGVudHM="}'
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json',
    }
    # owner, repo, path, branch
    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ["GITHUB_HEAD_REF"]
    existing_sha = get_sha('namrata1012', repo, file_path, branch)

    path, file_extension = os.path.splitext(file_path)
    split_path = path.split('/')
    filename = split_path[-1]

    generated_json_path = f'generated_files/json_files/{filename}.json'

    print(branch, existing_sha)
    url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/contents/{generated_json_path}'
    print(url)
    encoded_content = base64.b64encode(file_content.encode()).decode()
    payload = {
        'message': 'Update file via GitHub Actions',
        'content': encoded_content,
        'branch': branch,
        'sha':existing_sha
    }

# Make the API request to update the file
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
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