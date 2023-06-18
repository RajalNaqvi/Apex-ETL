import os
import json

directory = f'{os.getcwd()}/.local'
pipelines_directory = f"{directory}/pipelines"
connections_directory = f"{directory}/connections"
dirs = [directory,pipelines_directory,connections_directory]
json_files_data = None

def create_con_directory():
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")

def read_all_connection_configs(configs):
    json_files_data=[]
    for config in configs:
        file_path = os.path.join(connections_directory, f"{config}.json")
        with open(file_path) as json_file:
            json_data = json.load(json_file)
            json_data_with_filename = {
                'filename': config,
                'data': json_data
            }
            json_files_data.append(json_data_with_filename)
    return json_files_data

def store_connection_config(filename,json_data):
    try:
        with open(f"{connections_directory}/{filename}.json", 'w') as file:
            json.dump(json_data, file, indent=4)
            return True
    except Exception as e:
        return False

def get_all_connection_configs():
    return [
        filename.replace(".json", "")
        for filename in os.listdir(connections_directory)
        if filename.endswith('.json')
    ]

def read_config(config):
    json_data_with_filename = {}
    file_path = os.path.join(connections_directory, f"{config}.json")
    try:
        with open(file_path) as json_file:
            json_data = json.load(json_file)
            json_data_with_filename = {
                'filename': config,
                'data': json_data
            }
    except Exception as e:
        return json_data_with_filename
    return json_data_with_filename

def read_all_connection_configs():
    python_data = []
    jdbc_data = []
    configs = get_all_connection_configs()
    for config in configs:
        with open(f"{connections_directory}/{config}.json") as json_file:
            data = json.load(json_file)

        if data.get('connection_type') == 'python':
            python_data.append({"connection_name":config,"connection":data})
        elif data.get('connection_type') == 'jdbc':
            jdbc_data.append({"connection_name":config,"connection":data})
                
    return {"python": python_data,"java": jdbc_data}

def store_pipeline_config(config):
    if os.path.exists(f"{pipelines_directory}/" + config["integration_name"] + ".json"):
        return (False, "Integration already exists")
    try:
        with open(f"{pipelines_directory}/" + config["integration_name"] + ".json", 'w') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        return (False,str(e))
    del config["run_details"]
    return (True, config)

def read_all_pipeline_configs():
    return [
        filename.replace(".json", "")
        for filename in os.listdir(pipelines_directory)
        if filename.endswith('.json')
    ]

def read_pipeline_detals(pipeline):
    json_data = {}
    file_path = os.path.join(pipelines_directory, f"{pipeline}.json")
    try:
        with open(file_path) as json_file:
            json_data = json.load(json_file)["run_details"]
    except Exception as e:
        return json_data
    return json_data


